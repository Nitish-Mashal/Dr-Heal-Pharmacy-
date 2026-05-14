console.log("CUSTOM LIST JS LOADED");

$(document).ready(function () {

    const waitForProductList = setInterval(() => {

        if (
            typeof webshop !== "undefined" &&
            webshop.ProductList
        ) {

            clearInterval(waitForProductList);

            console.log("OVERRIDING ProductList");

            webshop.ProductList.prototype.get_image_html =
                function (item, title, settings) {

                    let image =
                        item.website_image ||
                        "/files/placeholder-medicine.jpeg";

                    let wishlist_enabled =
                        !item.has_variants &&
                        settings.enable_wishlist;

                    return `
                        <div class="col-2 border text-center rounded list-image">

                            <a class="product-link product-list-link"
                                href="/${item.route || '#'}">

                                <img
                                    itemprop="image"
                                    class="website-image h-100 w-100"
                                    alt="${title}"
                                    src="${image}">

                            </a>

                            ${wishlist_enabled
                            ? this.get_wishlist_icon(item)
                            : ''
                        }

                        </div>
                    `;
                };

            console.log("PLACEHOLDER OVERRIDE APPLIED");

        }

    }, 300);

});