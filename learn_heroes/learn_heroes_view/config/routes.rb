Rails.application.routes.draw do
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html

  root 'hero_stats#index'

  get 'check_stat', to: 'hero_stats#check_stat'

end
