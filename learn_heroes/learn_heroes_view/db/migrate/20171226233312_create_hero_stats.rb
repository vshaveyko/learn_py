class CreateHeroStats < ActiveRecord::Migration[5.1]
  def change
    create_table :hero_stats do |t|
      t.references :hero, foreign_key: true
      t.references :matchup, foreign_key: true

      t.integer :num_win
      t.integer :num_loss

      t.timestamps
    end

    add_index :hero_stats, [:hero_id, :matchup_id], unique: true
  end
end
