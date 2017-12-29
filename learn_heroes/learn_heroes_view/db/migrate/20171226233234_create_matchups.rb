class CreateMatchups < ActiveRecord::Migration[5.1]
  def change
    create_table :matchups do |t|
      t.integer :ally_heroes,  array: true, index: true
      t.integer :enemy_heroes, array: true, index: true

      t.timestamps
    end

    add_index :matchups, [:ally_heroes, :enemy_heroes], unique: true
  end
end
