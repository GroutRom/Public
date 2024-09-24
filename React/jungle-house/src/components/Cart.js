function Cart() {
    const monsteraPrice = 8
    const lierrePrice = 10
    const flowerPrice = 15

    return (
        <div>
            <h2>Panier</h2>
            <ul>
                <li>Monstera : {monsteraPrice}€</li>
                <li>Lierre : {lierrePrice}€</li>
                <li>Bouquet de fleurs : {flowerPrice}€</li>
            </ul>
            <p> Total : {monsteraPrice + lierrePrice + flowerPrice}€</p>
        </div>
    );

}

export default Cart;