import json
import requests


class ErrorSave(Exception):
    pass


class Parser_Metro():
    '''Класс для парсинга сайта https://online.metro-cc.ru/.'''
    def __init__(self):
        self.cookies = {
        'spid': '1686383066844_64d67cdbe620f71185a3008c2a6cf736_s015qsdw2iuk786v',
        '_slid': '648429de88d87966eb025167',
        '_gcl_au': '1.1.587489401.1686383074',
        'metro_user_id': '4a931c48f7646f96208b3b65ad2cc116',
        'tmr_lvid': '4d4b7920c94dd0dedfb40468457c0115',
        'tmr_lvidTS': '1686383080944',
        '_ym_uid': '1686383082501465087',
        '_ym_d': '1686383082',
        'uxs_uid': 'ac0d5b50-0762-11ee-b0bb-1395a7b7aaa9',
        'fam_user': '6 5',
        '_slid_server': '648429de88d87966eb025167',
        '_gid': 'GA1.2.2124191693.1686475908',
        '_slfreq': '633ff97b9a3f3b9e90027740%3A633ffa4c90db8d5cf00d7810%3A1686483111',
        'metro_api_session': 'QUwpIK7k2LS1OZCiRpGzVNDUuptdJ6leI4QXCAc3',
        '_ym_isad': '2',
        '_ga': 'GA1.2.1549265350.1686383084',
        'mindboxDeviceUUID': '7e5d654b-2f47-4077-927e-67ddd81b311f',
        'directCrm-session': '%7B%22deviceGuid%22%3A%227e5d654b-2f47-4077-927e-67ddd81b311f%22%7D',
        '_ga_VHKD93V3FV': 'GS1.1.1686472418.7.1.1686478751.0.0.0',
        'spsc': '1686478764050_01792ab7098a9bdca65c5cab204843ac_a5476469b72f558bb72e6aae99c6a060',
    }
        self.headers = {
        'authority': 'api.metro-cc.ru',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-AU,ru;q=0.9,en-VI;q=0.8,en;q=0.7,ru-RU;q=0.6,en-US;q=0.5',
        'content-type': 'application/json',
        # 'cookie': 'spid=1686383066844_64d67cdbe620f71185a3008c2a6cf736_s015qsdw2iuk786v; _slid=648429de88d87966eb025167; _gcl_au=1.1.587489401.1686383074; metro_user_id=4a931c48f7646f96208b3b65ad2cc116; tmr_lvid=4d4b7920c94dd0dedfb40468457c0115; tmr_lvidTS=1686383080944; _ym_uid=1686383082501465087; _ym_d=1686383082; uxs_uid=ac0d5b50-0762-11ee-b0bb-1395a7b7aaa9; fam_user=6 5; _slid_server=648429de88d87966eb025167; _gid=GA1.2.2124191693.1686475908; _slfreq=633ff97b9a3f3b9e90027740%3A633ffa4c90db8d5cf00d7810%3A1686483111; metro_api_session=QUwpIK7k2LS1OZCiRpGzVNDUuptdJ6leI4QXCAc3; _ym_isad=2; _ga=GA1.2.1549265350.1686383084; mindboxDeviceUUID=7e5d654b-2f47-4077-927e-67ddd81b311f; directCrm-session=%7B%22deviceGuid%22%3A%227e5d654b-2f47-4077-927e-67ddd81b311f%22%7D; _ga_VHKD93V3FV=GS1.1.1686472418.7.1.1686478751.0.0.0; spsc=1686478764050_01792ab7098a9bdca65c5cab204843ac_a5476469b72f558bb72e6aae99c6a060',
        'origin': 'https://online.metro-cc.ru',
        'referer': 'https://online.metro-cc.ru/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    
    def scrape_metro_shop_category(self, json_data, document):
        '''Получаем полный блок ответа от нужного нам эндпоинта.'''
        response = requests.post('https://api.metro-cc.ru/products-api/graph', cookies=self.cookies, headers=self.headers, json=json_data).json()
        quantity = response.get('data').get('category').get('filters').get('facets')[0].get('total')
        json_data['variables']['size'] = quantity
        response = requests.post('https://api.metro-cc.ru/products-api/graph', cookies=self.cookies, headers=self.headers, json=json_data).json()
        with open(document, 'w', encoding='utf-8') as file:
            json.dump(response, file, ensure_ascii=False, indent=4)
        # return response

    def save_result_json(self, document_for_preresult, document):
        '''Достаем нужные для нас данные из json файла и сохраняем в файл с результатами.'''
        with open(document_for_preresult, 'r', encoding='utf-8') as file:
            products_data = json.load(file)['data']['category']['products']

        if len(products_data) != 0:
            data = {}           
            for item in products_data:
                product_id = item.get('id')
                product_name = item.get('name')
                product_url = 'https://online.metro-cc.ru' + item.get('url')
                product_manufacturer = item.get('manufacturer').get('name')
                product_price = item.get('stocks')[0].get('prices_per_unit').get('old_price')
                # если основная цена равна null, то скидки на товар нет и его регулярная цена равна цене в нынешний момент
                if product_price == None:
                    product_price = item.get('stocks')[0].get('prices_per_unit').get('offline')['price']
                    product_price_discount = None
                else:
                    product_price_discount = item.get('stocks')[0].get('prices_per_unit').get('offline')['price']

                data[product_name] = {
                    'product_id': product_id,
                    'url': product_url,
                    'manufacturer': product_manufacturer,
                    'price': product_price,
                    'price_discount': product_price_discount
                }

            with open(document, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        else:
            raise ErrorSave

    def main(self, city, store_id):
        json_data = {
            'query': '\n  query Query($storeId: Int!, $slug: String!, $attributes:[AttributeFilter], $filters: [FieldFilter], $from: Int!, $size: Int!, $sort: InCategorySort, $in_stock: Boolean, $eshop_order: Boolean, $is_action: Boolean, $price_levels: Boolean) {\n    category (storeId: $storeId, slug: $slug, inStock: $in_stock, eshopAvailability: $eshop_order, isPromo: $is_action, priceLevels: $price_levels) {\n      id\n      name\n      slug\n      id\n      parent_id\n      meta {\n        description\n        h1\n        title\n        keywords\n      }\n      disclaimer\n      description {\n        top\n        main\n        bottom\n      }\n#      treeBranch {\n#        id\n#        name\n#        slug\n#        children {\n#          category_type\n#          id\n#          name\n#          slug\n#          children {\n#            category_type\n#            id\n#            name\n#            slug\n#            children {\n#              category_type\n#              id\n#              name\n#              slug\n#              children {\n#                category_type\n#                id\n#                name\n#                slug\n#              }\n#            }\n#          }\n#        }\n#      }\n      breadcrumbs {\n        category_type\n        id\n        name\n        parent_id\n        parent_slug\n        slug\n      }\n      promo_banners {\n        id\n        image\n        name\n        category_ids\n        virtual_ids\n        type\n        sort_order\n        url\n        is_target_blank\n        analytics {\n          name\n          category\n          brand\n          type\n          start_date\n          end_date\n        }\n      }\n\n\n      dynamic_categories(from: 0, size: 9999) {\n        slug\n        name\n        id\n      }\n      filters {\n        facets {\n          key\n          total\n          filter {\n            id\n            name\n            display_title\n            is_list\n            is_main\n            text_filter\n            is_range\n            category_id\n            category_name\n            values {\n              slug\n              text\n              total\n            }\n          }\n        }\n      }\n      total\n      prices {\n        max\n        min\n      }\n      pricesFiltered {\n        max\n        min\n      }\n      products(attributeFilters: $attributes, from: $from, size: $size, sort: $sort, fieldFilters: $filters)  {\n        health_warning\n        limited_sale_qty\n        id\n        slug\n        name\n        name_highlight\n        article\n        is_target\n        category_id\n        url\n        images\n        pick_up\n        icons {\n          id\n          badge_bg_colors\n          caption\n          image\n          type\n          is_only_for_sales\n          stores\n          caption_settings {\n            colors\n            text\n          }\n          stores\n          sort\n          image_png\n          image_svg\n          description\n          end_date\n          start_date\n          status\n        }\n        manufacturer {\n          id\n          image\n          name\n        }\n        packing {\n          size\n          type\n          pack_factors {\n            instamart\n          }\n        }\n        stocks {\n          value\n          text\n          eshop_availability\n          scale\n          prices_per_unit {\n            old_price\n            offline {\n              price\n              old_price\n              type\n              offline_discount\n              offline_promo\n            }\n            price\n            is_promo\n            levels {\n              count\n              price\n            }\n            discount\n          }\n          prices {\n            price\n            is_promo\n            old_price\n            offline {\n              old_price\n              price\n              type\n              offline_discount\n              offline_promo\n            }\n            levels {\n              count\n              price\n            }\n            discount\n          }\n        }\n      }\n    }\n  }\n',
            'variables': {
                'isShouldFetchOnlyProducts': True,
                'slug': 'chipsy-suhari-sneki',  # при смене здесь слага можно получить данные о товарах из других категорий
                'storeId': None,
                'sort': 'default',
                'size': 0,
                'from': 0,
                'filters': [],
                'attributes': [],
                'in_stock': True,
                'eshop_order': False,
            },
        }
        json_data['variables']['storeId'] = store_id
        document_for_preresult = 'preliminary_result_for_' + city + '.json'
        self.scrape_metro_shop_category(json_data, document_for_preresult)
        document_for_result = 'result_for_' + city + '.json'
        try:
            self.save_result_json(document_for_preresult, document_for_result)
            print(f'Сохранение произошло успешно в файл: {document_for_result}')
        except ErrorSave:
            print('Ошибка сохранения')


if __name__ == '__main__':
    parser = Parser_Metro()
    cities = {
        'Moscow': 10,
        'SPb': 15
    }
    for key, value in cities.items():
        parser.main(city=key, store_id=value)
