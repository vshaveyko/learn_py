class HeroStatsController < ApplicationController

  before_action do
    @heroes = Hero.all
  end

  def check_stat
    @current_stats = Matchup.find_by(strong_params)&.hero_stats

    render :index
  end

private

  def strong_params
    params.permit(
      ally_heroes: [],
      enemy_heroes: []
    )
  end

end
