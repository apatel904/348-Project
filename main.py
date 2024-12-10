from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="arya2003",
        database="NFL"
    )

# Home route with navigation buttons
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_team', methods=['GET', 'POST'])
def add_team():
    if request.method == 'POST':
        team_name = request.form['name']
        team_city = request.form['city']
        team_division = request.form['division']
        team_num_wins = request.form['num_wins']
        team_num_losses = request.form['num_loses']

        conn = get_db_connection()
        cursor = conn.cursor()
        insert_team_query = """
        INSERT INTO Teams (name, city, division, num_wins, num_loses) 
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_team_query, (team_name, team_city, team_division, team_num_wins, team_num_losses))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('home'))

    return render_template('add_team.html')

@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        player_name = request.form['name']
        team_id = request.form['team_id']
        position = request.form['position']
        age = request.form['age']

        conn = get_db_connection()
        cursor = conn.cursor()
        insert_player_query = """
        INSERT INTO Players (team_id, name, position, age) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_player_query, (team_id, player_name, position, age))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('home'))

    return render_template('add_player.html')


@app.route('/remove_team', methods=['GET', 'POST'])
def remove_team():
    if request.method == 'POST':
        team_name = request.form['name']

        conn = get_db_connection()
        cursor = conn.cursor()
        delete_team_query = "DELETE FROM Teams WHERE name = %s"
        cursor.execute(delete_team_query, (team_name,))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('home'))

    return render_template('remove_team.html')

@app.route('/remove_player', methods=['GET', 'POST'])
def remove_player():
    if request.method == 'POST':
        player_name = request.form['name']

        conn = get_db_connection()
        cursor = conn.cursor()
        delete_player_query = "DELETE FROM Players WHERE name = %s"
        cursor.execute(delete_player_query, (player_name,))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('home'))

    return render_template('remove_player.html')

@app.route('/edit_player', methods=['GET', 'POST'])
def edit_player():
    if request.method == 'POST':
        player_id = request.form['player_id']
        name = request.form['name']
        position = request.form['position']
        age = request.form['age']
        team_id = request.form['team_id']
        
        conn = mysql.connector.connect(host="localhost", user="root", password='arya2003', database='NFL')
        cursor = conn.cursor()
        
        update_query = """UPDATE Players 
                          SET name = %s, position = %s, age = %s, team_id = %s 
                          WHERE player_id = %s"""
        cursor.execute(update_query, (name, position, age, team_id, player_id))
        conn.commit()
        
        cursor.close()
        conn.close()
        return redirect(url_for('home'))  

    return render_template('edit_player.html')


@app.route('/add_game', methods=['GET', 'POST'])
def add_game():
    if request.method == 'POST':
        home_team_id = request.form['home_team_id']
        away_team_id = request.form['away_team_id']
        game_date = request.form['game_date']
        home_team_score = request.form['home_team_score']
        away_team_score = request.form['away_team_score']
        winner_team_id = request.form['winner_team_id']
        
        conn = mysql.connector.connect(host="localhost", user="root", password='arya2003', database='NFL')
        cursor = conn.cursor()
        
        insert_query = """INSERT INTO Games (home_team_id, away_team_id, date, home_team_score, away_team_score, winner_team_id) 
                          VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(insert_query, (home_team_id, away_team_id, game_date, home_team_score, away_team_score, winner_team_id))
        conn.commit()
        
        cursor.close()
        conn.close()
        return redirect(url_for('home'))  

    conn = mysql.connector.connect(host="localhost", user="root", password='arya2003', database='NFL')
    cursor = conn.cursor()
    cursor.execute("SELECT team_id, name FROM Teams")  
    teams = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('add_game.html', teams=teams)




@app.route('/add_quarterback_stats', methods=['GET', 'POST'])
def add_quarterback_stats():
    if request.method == 'POST':
        player_id = request.form['player_id']
        passing_yards = request.form['passing_yards']
        touchdowns = request.form['touchdowns']
        interceptions = request.form['interceptions']
        game_id = request.form['game_id']

        # uses stored procedure 
        conn = mysql.connector.connect(host="localhost", user="root", password='arya2003', database='NFL')
        cursor = conn.cursor()
        cursor.callproc('addQBStat', (player_id, passing_yards, touchdowns, interceptions, game_id))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('home')) 
    return render_template('add_quarterback_stats.html')



@app.route('/add_runningback_stats', methods=['GET', 'POST'])
def add_runningback_stats():
    if request.method == 'POST':
        player_id = request.form['player_id']
        carries = request.form['carries']
        yards = request.form['yards']
        touchdowns = request.form['touchdowns']
        game_id = request.form['game_id']

        # Uses stored procedure 
        conn = mysql.connector.connect(host="localhost", user="root", password='arya2003', database='NFL')
        cursor = conn.cursor()
        cursor.callproc('addRBStat', (player_id, carries, yards, touchdowns, game_id))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('home')) 
    return render_template('add_runningback_stats.html')



@app.route('/add_receiver_stats', methods=['GET', 'POST'])
def add_receiver_stats():
    if request.method == 'POST':
        player_id = request.form['player_id']
        receptions = request.form['receptions']
        yards = request.form['yards']
        targets = request.form['targets']
        touchdowns = request.form['touchdowns']
        game_id = request.form['game_id']

        # Uses stored procedure
        conn = mysql.connector.connect(host="localhost", user="root", password='arya2003', database='NFL')
        cursor = conn.cursor()
        cursor.callproc('addWRStat', (player_id, receptions, yards, targets, touchdowns, game_id))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('home')) 
    return render_template('add_receiver_stats.html')


@app.route('/report_qb_stats', methods=['GET', 'POST'])
def report_qb_stats():
    filters = {
        'player_id': request.form.get('player_id'),
        'min_yards': request.form.get('min_yards'),
        'min_touchdowns': request.form.get('min_touchdowns'),
        'game_id': request.form.get('game_id'),
    }
    
    query = """
        SELECT player_id, passing_yards, touchdowns, interceptions, game_id
        FROM QB_Stats
        WHERE 1=1
    """
    
    params = [] 
    if filters['player_id']:
        query += " AND player_id = %s"
        params.append(filters['player_id'])
    if filters['min_yards']:
        query += " AND passing_yards >= %s"
        params.append(filters['min_yards'])
    if filters['min_touchdowns']:
        query += " AND touchdowns >= %s"
        params.append(filters['min_touchdowns'])
    if filters['game_id']:
        query += " AND game_id = %s"
        params.append(filters['game_id'])
    
    query += " ORDER BY passing_yards DESC"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('report_qb_stats.html', results=results, filters=filters)


@app.route('/report_rb_stats', methods=['GET', 'POST'])
def report_rb_stats():
    filters = []
    values = []

    touchdowns = request.form.get('touchdowns')
    carries = request.form.get('carries')
    yards = request.form.get('yards')

    query = "SELECT player_id, carries, yards, touchdowns, game_id FROM RB_Stats"
    if touchdowns:
        filters.append("touchdowns >= %s")
        values.append(touchdowns)
    if carries:
        filters.append("carries >= %s")
        values.append(carries)
    if yards:
        filters.append("yards >= %s")
        values.append(yards)

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += " ORDER BY yards DESC"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, values)
    results = cursor.fetchall()
    cursor.close()

    return render_template('report_rb_stats.html', results=results)



if __name__ == "__main__":
    app.run(debug=True)
