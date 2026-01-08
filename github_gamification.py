import requests
import math
import os

def get_github_stats(username):
    url = f"https://api.github.com/users/{username}"
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    headers = {"Accept": "application/vnd.github.v3+json"}
    user = requests.get(url, headers=headers).json()
    repos = requests.get(repos_url, headers=headers).json()
    
    stars = sum(repo.get('stargazers_count', 0) for repo in repos)
    forks = sum(repo.get('forks_count', 0) for repo in repos)
    public_repos = user.get('public_repos', 0)
    followers = user.get('followers', 0)
    
    return {
        'stars': stars,
        'forks': forks,
        'public_repos': public_repos,
        'followers': followers
    }

def calculate_gamification(stats):
    # Pontuação baseada em estrelas, forks, seguidores e repositórios
    score = stats['stars'] * 5 + stats['forks'] * 3 + stats['followers'] * 10 + stats['public_repos'] * 2
    # Nível: cada 500 pontos sobe de nível
    level = math.floor(score / 500) + 1
    # Insígnias
    badges = []
    if stats['stars'] > 50:
        badges.append('⭐ Caçador de Estrelas')
    if stats['forks'] > 20:
        badges.append('🍴 Mestre dos Forks')
    if stats['followers'] > 10:
        badges.append('👥 Influencer')
    if stats['public_repos'] > 10:
        badges.append('📦 Prolífico')
    return score, level, badges

def render_markdown(score, level, badges):
    badges_md = ' '.join([f'![badge](https://img.shields.io/badge/{b.replace(" ","%20")}-blueviolet?style=for-the-badge)' for b in badges])
    return f"""
## 🕹️ GitHub Gamificação

- **Pontuação:** `{score}`
- **Nível:** `{level}`
- **Insígnias:** {badges_md if badges else 'Nenhuma ainda, continue jogando!'}
"""

def main():
    username = os.environ.get('GITHUB_USERNAME', 'luarafael')
    stats = get_github_stats(username)
    score, level, badges = calculate_gamification(stats)
    md = render_markdown(score, level, badges)
    with open('GITHUB_GAME_STATS.md', 'w', encoding='utf-8') as f:
        f.write(md)

if __name__ == "__main__":
    main()
