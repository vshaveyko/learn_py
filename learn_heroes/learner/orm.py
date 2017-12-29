import postgresql
db = postgresql.open('pq://postgres:postgres@localhost:5432/learn_heroes_view_development')

# set updated_at to use RETURNING
create_matchup = db.prepare("""

    INSERT INTO matchups ("ally_heroes", "enemy_heroes", "created_at", "updated_at")
           VALUES ($1, $2, now(), now())
           ON CONFLICT (ally_heroes, enemy_heroes) DO UPDATE SET updated_at=now()
           RETURNING ID

""")

lookup_matchup = db.prepare("SELECT id FROM matchups WHERE ally_heroes = $1::int[] AND enemy_heroes = $2::int[]")

def find_or_create_matchup(team1, team2):
    return create_matchup.first(team1, team2)

def generate_hero_stats_upsert_statement(matchup):
    ally, enemy = matchup

    ally_heroes = ','.join(str(al) for al in ally)
    enemy_heroes = ','.join(str(en) for en in enemy)

    matchup_upsert = f"""

        INSERT INTO matchups ("ally_heroes", "enemy_heroes", "created_at", "updated_at")
               VALUES ( array[{ally_heroes}]::integer[], array[{enemy_heroes}]::integer[], now(), now() )
               ON CONFLICT (ally_heroes, enemy_heroes) DO UPDATE SET updated_at=now()
               RETURNING ID

    """

    return f"""
        WITH m_ups AS ({ matchup_upsert })

        INSERT INTO hero_stats (num_win, num_loss, hero_id, matchup_id, created_at, updated_at)
               SELECT unnest(%(num_wins)s),
                      unnest(%(num_loss)s),
                      unnest(%(hero_ids)s),
                      (SELECT id FROM m_ups),
                      now(), now()
               ON CONFLICT (hero_id, matchup_id)
                  DO UPDATE SET num_win = hero_stats.num_win + excluded.num_win, num_loss = hero_stats.num_loss + excluded.num_loss

    """

add_hero_stats = db.prepare("""

    INSERT INTO hero_stats (num_win, num_loss, hero_id, matchup_id, created_at, updated_at)
           VALUES ( $1, $2, $3, $4, now(), now() )
           ON CONFLICT (hero_id, matchup_id)
              DO UPDATE SET num_win = hero_stats.num_win + $1, num_loss = hero_stats.num_loss + $2

""")

def add_hero_stat_for_matchup(matchup_id, hero_id, is_win):
    if is_win:
        top_incr = 1
    else:
        top_incr = 0

    bot_incr = 1

    add_hero_stats(top_incr, bot_incr, hero_id, matchup_id)
