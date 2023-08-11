import tkinter as tk
from tkinter import scrolledtext
import requests

class GitHubProjectsSearcher:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub Projects Searcher")
        
        self.type_var = tk.StringVar(value="repositories")
        self.stars_var = tk.StringVar(value="")
        self.language_var = tk.StringVar(value="")
        self.num_projects_var = tk.StringVar(value="10")
        
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self.root, text="Type:").grid(row=0, column=0, sticky="e")
        tk.Label(self.root, text="Number of Stars:").grid(row=1, column=0, sticky="e")
        tk.Label(self.root, text="Programming Language:").grid(row=2, column=0, sticky="e")
        tk.Label(self.root, text="Number of Projects:").grid(row=3, column=0, sticky="e")
        
        tk.Entry(self.root, textvariable=self.type_var).grid(row=0, column=1, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.stars_var).grid(row=1, column=1, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.language_var).grid(row=2, column=1, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.num_projects_var).grid(row=3, column=1, padx=10, pady=5)
        
        tk.Button(self.root, text="Search", command=self.search_projects).grid(row=4, column=1, pady=10)
        
        self.result_text = scrolledtext.ScrolledText(self.root, width=50, height=20)
        self.result_text.grid(row=5, columnspan=2, padx=10, pady=10)
    
    def search_projects(self):
        params = {
            'q': self.construct_query(),
            'sort': 'stars',
            'order': 'desc',
            'per_page': self.num_projects_var.get()
        }
        
        response = requests.get('https://api.github.com/search/repositories', params=params)
        projects = response.json().get('items', [])
        
        self.display_projects(projects)
    
    def construct_query(self):
        query_parts = []
        
        if self.type_var.get():
            query_parts.append(f'type:{self.type_var.get()}')
        if self.stars_var.get() != "":
            query_parts.append(f'stars:{self.stars_var.get()}')
        if self.language_var.get():
            query_parts.append(f'language:{self.language_var.get()}')
        
        return ' '.join(query_parts)
    
    def display_projects(self, projects):
        self.result_text.delete('1.0', tk.END)
        
        for project in projects:
            name = project.get('name', 'N/A')
            description = project.get('description', 'N/A')
            stars = project.get('stargazers_count', 'N/A')
            url = project.get('html_url', 'N/A')
            
            result = f"Project Name: {name}\nDescription: {description}\nStars: {stars}\nURL: {url}\n\n"
            self.result_text.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubProjectsSearcher(root)
    root.mainloop()
