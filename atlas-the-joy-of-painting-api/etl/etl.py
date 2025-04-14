import pandas as pd
import pymysql
import ast

# ---------- DB CONNECTION ----------
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='0Akley11',
    database='joy_of_painting'
)
cursor = conn.cursor()

def insert_season(season_number):
    cursor.execute("INSERT IGNORE INTO seasons (season_number) VALUES (%s)", (season_number,))
    cursor.execute("SELECT id FROM seasons WHERE season_number = %s", (season_number,))
    return cursor.fetchone()[0]

def insert_episode(season_number, episode_number, title, date):
    season_id = insert_season(season_number)
    cursor.execute("""
        INSERT INTO episodes (season_id, episode_number, title, painting_name, broadcast_date)
        VALUES (%s, %s, %s, %s, %s)
    """, (season_id, episode_number, title, title, date))
    return cursor.lastrowid

def get_episode_id(season_number, episode_number):
    cursor.execute("""
        SELECT e.id FROM episodes e
        JOIN seasons s ON e.season_id = s.id
        WHERE s.season_number = %s AND e.episode_number = %s
    """, (season_number, episode_number))
    result = cursor.fetchone()
    return result[0] if result else None

def insert_color(color):
    cursor.execute("INSERT IGNORE INTO colors (name) VALUES (%s)", (color,))
    cursor.execute("SELECT id FROM colors WHERE name = %s", (color,))
    return cursor.fetchone()[0]

def insert_subject(subject):
    cursor.execute("INSERT IGNORE INTO subjects (name) VALUES (%s)", (subject,))
    cursor.execute("SELECT id FROM subjects WHERE name = %s", (subject,))
    return cursor.fetchone()[0]

# ---------- ETL: EPISODES ----------
for i, row in episodes_df.iterrows():
    raw = row['raw']
    if '(' not in raw:
        continue

    title, date = raw.rsplit('(', 1)
    title = title.strip().title()
    broadcast_date = pd.to_datetime(date.strip(')'), errors='coerce')

    if pd.isna(broadcast_date):
        continue

    broadcast_date = broadcast_date.date()

    season_number = (i // 13) + 1
    episode_number = (i % 13) + 1

    insert_episode(season_number, episode_number, title, broadcast_date)

# ---------- ETL: COLORS ----------
colors_df = pd.read_csv('data/colors_used.csv')
colors_df['colors_list'] = colors_df['colors'].apply(ast.literal_eval)

for _, row in colors_df.iterrows():
    episode_id = get_episode_id(row['season'], row['episode'])
    if episode_id:
        for color in row['colors_list']:
            color_id = insert_color(color.strip())
            cursor.execute("INSERT IGNORE INTO episode_colors (episode_id, color_id) VALUES (%s, %s)", (episode_id, color_id))

# ---------- ETL: SUBJECTS ----------
subjects_df = pd.read_csv('data/subjects.csv')
subject_cols = subjects_df.columns[2:]

for _, row in subjects_df.iterrows():
    ep_code = row['EPISODE']
    season_number = int(ep_code[1:3])
    episode_number = int(ep_code[4:6])
    episode_id = get_episode_id(season_number, episode_number)

    if episode_id:
        for subject in subject_cols:
            if row[subject] == 1:
                subject_id = insert_subject(subject.replace("_", " ").title())
                cursor.execute("INSERT IGNORE INTO episode_subjects (episode_id, subject_id) VALUES (%s, %s)", (episode_id, subject_id))

conn.commit()
cursor.close()
conn.close()
print("Happy Accident")
