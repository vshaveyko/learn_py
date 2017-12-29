# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20171226233312) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "hero_stats", force: :cascade do |t|
    t.bigint "hero_id"
    t.bigint "matchup_id"
    t.integer "num_win"
    t.integer "num_loss"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["hero_id", "matchup_id"], name: "index_hero_stats_on_hero_id_and_matchup_id", unique: true
    t.index ["hero_id"], name: "index_hero_stats_on_hero_id"
    t.index ["matchup_id"], name: "index_hero_stats_on_matchup_id"
  end

  create_table "heros", force: :cascade do |t|
    t.string "name"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "matchups", force: :cascade do |t|
    t.integer "ally_heroes", array: true
    t.integer "enemy_heroes", array: true
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["ally_heroes", "enemy_heroes"], name: "index_matchups_on_ally_heroes_and_enemy_heroes", unique: true
    t.index ["ally_heroes"], name: "index_matchups_on_ally_heroes"
    t.index ["enemy_heroes"], name: "index_matchups_on_enemy_heroes"
  end

  add_foreign_key "hero_stats", "heros"
  add_foreign_key "hero_stats", "matchups"
end
