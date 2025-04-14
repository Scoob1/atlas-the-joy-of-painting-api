from flask import Flask, request, jsonify
import pymysql
from datetime import datetime

app = Flask(__name__)

# --- DB Connection ---
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='0Akley11',
    database='joy_of_painting',
    cursorclass=pymysql.cursors.DictCursor
)

# --- Route: Filter Episodes ---
@app.route('/episodes', methods=['GET'])
def filter_episodes():
    colors = request.args.getlist('color')
    subjects = request.args.getlist('subject')
    month = request.args.get('month')
    match_all = request.args.get('match_all', 'false').lower() == 'true'

    filters = []
    joins = []

    if colors:
        joins.append("""
            JOIN episode_colors ec ON ec.episode_id = e.id
            JOIN colors c ON c.id = ec.color_id
        """)
        color_filter = "c.name IN ({})".format(','.join(['%s'] * len(colors)))
        filters.append(f"({color_filter})")

    if subjects:
        joins.append("""
            JOIN episode_subjects es ON es.episode_id = e.id
            JOIN subjects s ON s.id = es.subject_id
        """)
        subject_filter = "s.name IN ({})".format(','.join(['%s'] * len(subjects)))
        filters.append(f"({subject_filter})")

    if month:
        filters.append("MONTH(e.broadcast_date) = %s")

    base_query = """
        SELECT DISTINCT e.id, e.title, e.painting_name, e.broadcast_date,
               s.season_number, e.episode_number
        FROM episodes e
        JOIN seasons s ON e.season_id = s.id
        {}
    """.format(' '.join(set(joins)))

    if filters:
        logic = ' AND ' if match_all else ' OR '
        base_query += " WHERE " + logic.join(filters)

    base_query += " ORDER BY s.season_number, e.episode_number"

    values = []
    if colors:
        values.extend(colors)
    if subjects:
        values.extend(subjects)
    if month:
        month_number = datetime.strptime(month, "%B").month
        values.append(month_number)

    with conn.cursor() as cursor:
        cursor.execute(base_query, values)
        results = cursor.fetchall()

    return jsonify(results)

# --- Run Locally ---
if __name__ == '__main__':
    app.run(debug=True)

