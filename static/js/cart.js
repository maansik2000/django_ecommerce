var updateBtns = document.getElementsByClassName("update-cart");

for (i = 0; i < updateBtns.length; i++) {						//loop through the add to cart buttons, and add to the cart
  
  updateBtns[i].addEventListener("click", function () {			// loop the add event listener to all the buttons lengths and find which item is added
    
    var productId = this.dataset.product; 						//get the product id of which button is clicked
    var action = this.dataset.action; 							//get the product action like add or remove
    console.log("productId:", productId, "Action:", action);
    console.log("USER:", user); 								//print out the user status(anonymous or not)
    if (user == "AnonymousUser") {								//check if the user is anonymous or not
      
		addCookieItem(productId, action)
    } else {
      updateUserOrder(productId, action);						//function to add the data to the backend 
    }
  });
}

//function to puts the order in the backend with the fetch method
function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_Item/'								//backend url

		fetch(url, {
			method:'POST',										//post method where we will send the data 
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,						//csrf token from the main js csrf ajax token
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})	//product id and action are sent to the backend
		})
		.then((response) => {
		   return response.json();								// we gets json response or return the json response
		})
		.then((data) => {
		    console.log(data)									//we get the data in return and console it out
			location.reload();
		});
}

//this handle the cookies when the user is not logged in
function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}

