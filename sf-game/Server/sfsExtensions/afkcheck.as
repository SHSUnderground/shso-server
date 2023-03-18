 /* 
* Initializion point:
* 
* this function is called as soon as the extension
* is loaded in the server.
* 
* You can add here all the initialization code
* 
*/


var afkLoop


function init()
{
	trace("Extension AFKCHECK initialized")
	
	afkLoop = setInterval(function(){
	
		var zone = _server.getCurrentZone().getUserList()
		
		
		
		for(var i:int=0; i<zone.length; i++)
		{
		
			if(zone[i].getLastMessageTime() > 15000){
				
				trace("Kicking user")
				_server.disconnectUser(zone[i])
				
			}
		
		}
	
	},15000)
	
}


/*
* This method is called by the server when an extension
* is being removed / destroyed.
* 
* Always make sure to release resources like setInterval(s)
* open files etc in this method.
* 
* In this case we delete the reference to the databaseManager
*/
function destroy()
{
	trace("Extension destroyed")
}


/*
* 
* Handle Client Requests
* 
* cmd 		= a string with the client command to execute 
* params 	= list of parameters expected from the client
* user 		= the User object representing the sender
* fromRoom 	= the id of the room where the request was generated
* 
*/
