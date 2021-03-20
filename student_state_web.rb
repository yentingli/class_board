require "sinatra"
require 'sinatra/reloader' if development?
# also_reload 'text.txt'
# after_reload do
#   puts 'reloaded'
# end
require 'json'
set :bind, '0.0.0.0'
enable :sessions

get "/:student/:state" do 
  data ="#{params[:student]}, #{params[:state]}"
  File.open("file_#{params[:student]}.txt", 'w') { |file| file.write(data) }
  redirect '/'
end

get "/" do
  @Yenting = File.read('file_Yenting.txt')
  @Li = File.read('file_Li.txt')
  erb :page
end


# post '/post' do
#   push = JSON.parse(request.body.read)
#   puts "I got some JSON: #{push.inspect}"
#   data = push.inspect
#   #File.open('file.txt', 'w') { |file| file.write(data) }
#   data
# end

# get "/post" do
#   puts "!!! in get #{session[:student_state]}"
#   @student_state = session[:student_state]
#   erb :post
# end