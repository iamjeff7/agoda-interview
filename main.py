'''
TO-DO List
1. Top 10 most recent pull request
2. Top 10 most recent issues
'''

from github import Github
import json
import datetime


class PublicGitHubRepo:
    def __init__(self, credential_json_file):
        credential = json.load(open(credential_json_file))
        username = credential['username']
        password = credential['password']
        self.g = Github(username, password)

    def run(self):
        repo_name = input('Enter the repository name (format: owner/repository):\n')
        info_type = input('Enter the information type (pull-requests, issues):\n')
        self.get_top_10(repo_name, info_type)

    def get_top_10(self, repo_name, info_type):
        print('\n'*2)
        if info_type == 'pull-requests':
            print(f'Repository {repo_name} top 10 Pull requests are:')
            data = self.g.get_repo(repo_name).get_pulls()
        elif info_type == 'issues':
            print(f'Repository {repo_name} top 10 issues are:')
            data = self.g.get_repo(repo_name).get_issues()

        self.iterate_page(data, info_type)
    
    def iterate_page(self, pages, info_type):
        count_page = 0
        current_page = 0
        while True:
            page = pages.get_page(count_page)
            for idx, p in enumerate(page):
                self.format_info(p, info_type)
                count_page += 1
                if count_page == 10:
                    break
            count_page += 1
                
    def format_info(self, p, info_type):
        p_num = p.number
        created_at = p.created_at.strftime("%B %d, %Y")
        user = p.user.login
        state = p.state
        title = p.title
        if info_type == 'pull-requests':
            print(f'PR-{p_num} - {title}')
        elif info_type == 'issue':
            print(f'#{p_num} = {title}')
        
        print(f'Created by {user} on {created_at}')

        if info_type == 'pull-requests':
            print(f'PR is {state}\n')
        elif info_type == 'issue':
            print(f'Issue is {state}\n')


def main():
    repo = ['chromium/chromium']

    pgr = PublicGitHubRepo(credential_json_file='credential.json')
    pgr.run()


if __name__ == '__main__':
    main()

