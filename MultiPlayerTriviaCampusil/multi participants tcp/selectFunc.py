import select # the libary that allows to serve multiple costumers

#ready_to_read, ready_to_write, in_error = select.select(read_list, write_list, error_list)

#read_list - the array of sockets that we would like to check what is new about them
#write_list - the array of sockets that are avilable to access
#error_list - the array of sockets that we would want to know if an error has occured in thems
#the select function would put in the ready_to_read all the sockets that we can read from, namely those who contain new data
#select is a blocking function and won't finish until it finds something new in a socket? (idk) I think select check for new and if not find stop
#client_sockets the sockets that already exists
#server_socket the new sockets that want to communicate with the server (comes from attempt to acess the server) 