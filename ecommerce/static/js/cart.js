let updateBtns = document.getElementsByClassName('update-cart');

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        let productId = this.dataset.product // access custom html-attribut 'data-product'
        let action = this.dataset.action // access custom html-attribut 'data-action'
        console.log('productId:', productId, 'Action:', action);

        console.log('USER', user);
        if (user === 'AnonymousUser') {
            addCookieItem(productId, action);
        } else {
            updateUserOrder(productId, action);
        }
    })
}

function addCookieItem (productId, action) {
    console.log('User is not authenticated');

    if (action == 'add') {
        if (cart[productId] == undefined) { // check if cart has the productId in it
            cart[productId] = {'quantity':1}; // if not, initialize it with 1
        } else {
            cart[productId]['quantity'] += 1; // if yes, increase by 1
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1;

        if (cart[productId]['quantity'] <= 0) {
            console.log('Item should be deleted');
            delete cart[productId];
        }
    }

    console.log('Cart:', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload();
}

function updateUserOrder(productId, action){
    console.log('User is authenticated, sending data...');

    let url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId,'action':action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('data:', data);
        location.reload() // reload page
    });
}