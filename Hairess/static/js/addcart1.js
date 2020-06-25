/* cart functionality */
var click_cart = document.getElementsByClassName('click-cart');
var minus = document.getElementsByClassName('minus');
var plus = document.getElementsByClassName('plus');


for ( let i = 0; i < click_cart.length; i+=1){

	click_cart[i].addEventListener('click', function() {

		let productId = this.dataset.product;
		let action = this.dataset.action;

		
		if (action == 'add')
		{
			if (user == 'AnonymousUser')
			{
				addCart(productId, action, user)
			}else
			{
				addCart(productId, action, user)
			}
		}
	})
}

for ( let i = 0; i < minus.length; i+=1){

	minus[i].addEventListener('click', function() {

		let productId = this.dataset.product;
		let action = this.dataset.action;

		
		if (action == 'minus')
		{
			if (user == 'AnonymousUser')
			{
				addCart(productId, action, user)
			}else
			{
				addCart(productId, action, user)
			}
		}
	})
}


for ( let i = 0; i < plus.length; i+=1){

	plus[i].addEventListener('click', function() {

		let productId = this.dataset.product;
		let action = this.dataset.action;

		
		if (action == 'plus')
		{
			if (user == 'AnonymousUser')
			{
				addCart(productId, action, user)
			}else
			{
				addCart(productId, action, user)
			}
		}
	})
}


//sending product data to django
function addCart(productId, action, user){
	let url = '/api/'

	fetch(url, {
		method : 'POST',
		headers : {
			'Content-Type' : 'application/json',
			'X-CSRFToken' : csrftoken,
		},
		body : JSON.stringify({'productId' : productId , 'action' : action, 'user':user  })
	})
	.then(response => {
		return response.json()
	})
	.then(data => {
			console.log(data);	
			setTimeout(()=>{
             location.reload()
        	},2000)
	})
}

//remove from cart
var remove = document.getElementsByClassName('fa-close');

for ( let i = 0; i < remove.length; i+=1){

		remove[i].addEventListener('click', function() {

			let productId = this.dataset.product;
			let action = this.dataset.action;

			
			if (action == 'remove')
			{
				if (user == 'AnonymousUser')
				{
					removeCart(productId, action, user)
				}else
				{
					removeCart(productId, action, user)
				}
			}
		})
	}

	function removeCart(productId, action, user){
		let url = '/api/'

		fetch(url, {
			method : 'POST',
			headers : {
				'Content-Type' : 'application/json',
				'X-CSRFToken' : csrftoken,
			},
			body : JSON.stringify({'productId' : productId , 'action' : action, 'user':user  })
		}).then(response => {
			return response.json()
		}).then(data => {
				console.log(data);	
				setTimeout(()=>{
	             location.reload()
	        	},2000)
		})
	}
