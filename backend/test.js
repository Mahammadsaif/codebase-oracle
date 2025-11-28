function calculateTotal(items) {
    return items.reduce((sum, item) => sum + item.price, 0);
}

class ShoppingCart {
    constructor() {
        this.items = [];
    }
    
    addItem(product, price) {
        this.items.push({ product, price });
        return this.items.length;
    }
}

import { useState } from "react";
