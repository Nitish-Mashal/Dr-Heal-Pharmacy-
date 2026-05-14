import frappe


@frappe.whitelist(allow_guest=True)
def get_products_by_tag(tag):

    products = frappe.db.sql("""
        SELECT
            i.name AS item_code,
            i.item_name,

            wi.website_image AS image,

            (
                SELECT ip.price_list_rate
                FROM `tabItem Price` ip
                WHERE ip.item_code = i.name
                LIMIT 1
            ) AS standard_rate,

            wi.route

        FROM `tabItem` i

        INNER JOIN `tabTag Link` tl
            ON tl.document_name = i.name

        LEFT JOIN `tabWebsite Item` wi
            ON wi.item_code = i.name

        WHERE
            tl.tag = %s
            AND i.disabled = 0
            AND wi.published = 1

        ORDER BY i.modified DESC
        LIMIT 12
    """, tag, as_dict=True)

    for p in products:

        p["route"] = (
            f"/{p['route']}"
            if p.get("route")
            else "#"
        )

        p["image"] = (
            p.get("image")
            or "/files/placeholder-medicine.jpeg"
        )

    return products


@frappe.whitelist(allow_guest=True)
def get_product_tags():

    return frappe.db.sql("""
        SELECT DISTINCT tl.tag

        FROM `tabTag Link` tl

        INNER JOIN `tabTag` t
            ON t.name = tl.tag

        WHERE tl.document_type = 'Item'

        ORDER BY tl.tag
    """, as_dict=True)