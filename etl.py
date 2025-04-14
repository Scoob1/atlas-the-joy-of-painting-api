import csv
import json
import xml.etree.ElementTree as ET
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='youruser',
    password='yourpass',
    database='joy_of_painting'
)
cursor = conn.cursor()

def normalize_text(text):
    return text.strip().lower()

def insert_season(season_number):
    cursor.execute("INSERT IGNORE INTO seasons (season_number) VALUES (%s)", (season_number,))
    cursor.execute("SELECT id FROM seasons WHERE season_number = %s", (season_number,))
    return cursor.fetchone()[0]

def insert_episode(row):
    season_id = insert_season(int(row['season']))
    cursor.execute("""
        INSERT INTO episodes (season_id, episode_number, title, painting_name, broadcast_date)
        VALUES (%s, %s, %s, %s, %s)
    """, (season_id, int(row['episode']), row['title'], row['painting'], row['broadcast_date']))
    return cursor.lastrowid

def insert_subject(subject):
    subject = normalize_text(subject)
    cursor.execute("INSERT IGNORE INTO subjects (name) VALUES (%s)", (subject,))
    cursor.execute("SELECT id FROM subjects WHERE name = %s", (subject,))
    return cursor.fetchone()[0]

def insert_color(color):
    color = normalize_text(color)
    cursor.execute("INSERT IGNORE INTO colors (name) VALUES (%s)", (color,))
    cursor.execute("SELECT id FROM colors WHERE name = %s", (color,))
    return cursor.fetchone()[0]

def load_episodes_csv(path):
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            insert_episode(row)

def load_subjects_json(path):
    with open(path) as f:
        data = json.load(f)
        for entry in data:
            episode_id = get_episode_id(entry['title'])
            for subject in entry['subjects']:
                subject_id = insert_subject(subject)
                cursor.execute("INSERT IGNORE INTO episode_subjects (episode_id, subject_id) VALUES (%s, %s)", (episode_id, subject_id))

def load_colors_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()
    for episode in root.findall('episode'):
        title = episode.find('title').text
        episode_id = get_episode_id(title)
        for color in episode.findall('colors/color'):
            color_id = insert_color(color.text)
            cursor.execute("INSERT IGNORE INTO episode_colors (episode_id, color_id) VALUES (%s, %s)", (episode_id, color_id))

def get_episode_id(title):
    cursor.execute("SELECT id FROM episodes WHERE title = %s", (title,))
    result = cursor.fetchone()
    return result[0] if result else None

if __name__ == '__main__':
    load_episodes_csv('data/episodes.csv')
    load_subjects_json('data/subjects.json')
    load_colors_xml('data/colors.xml')
    conn.commit()
    cursor.close()
    conn.close()

