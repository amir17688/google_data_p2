from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class BacktoherrootsMixin(object):
    source = 'backtoherroots'

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        base_path = '//html'

        recipes_scopes = hxs.select(base_path)

        name_path = './/p[@id="title"]/text()'
        description_path = "descendant-or-self::p[@class and contains(concat(' ', normalize-space(@class), ' '), ' summary ')]/text()"
        image_path = './/img[@class="photo"]/@src'
        prepTime_path = './/span[@class="preptime"]/text()'
        cookTime_path = './/span[@class="cooktime"]/text()'
        recipeYield_path = './/p[@id="ingr_header"]/span[@class="single_recipe_text"]/text()'
        ingredients_path = './/li[@class="ingredient"]/text()'

        recipes = []

        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', response.url)
            il.add_value('description', r_scope.select(description_path).extract())

            il.add_value('prepTime', r_scope.select(prepTime_path).extract())
            il.add_value('cookTime', r_scope.select(cookTime_path).extract())
            il.add_value('recipeYield', r_scope.select(recipeYield_path).extract())

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                ingredients.append(i_scope.extract())

            il.add_value('ingredients', ingredients)

            recipes.append(il.load_item())

        return recipes


class BacktoherrootscrawlSpider(CrawlSpider, BacktoherrootsMixin):

    name = "backtoherroots.com"

    allowed_domains = ["backtoherroots.com", "www.recipage.com"]

    urls = [
        'http://www.recipage.com/recipes/6029332.html',
        'http://www.recipage.com/recipes/6017153.html',
        'http://www.recipage.com/recipes/6002821.html',
        'http://www.recipage.com/recipes/6006480.html',
        'http://www.recipage.com/recipes/6031769.html',
        'http://www.recipage.com/recipes/6034510.html',
        'http://www.recipage.com/recipes/6001225.html',
        'http://www.recipage.com/recipes/6003965.html',
        'http://www.recipage.com/recipes/6002321.html',
        'http://www.recipage.com/recipes/6001301.html',
        'http://www.recipage.com/recipes/6044259.html',
        'http://www.recipage.com/recipes/6002884.html',
        'http://www.recipage.com/recipes/6002113.html',
        'http://www.recipage.com/recipes/6024725.html',
        'http://www.recipage.com/recipes/6022195.html',
        'http://www.recipage.com/recipes/6031400.html',
        'http://www.recipage.com/recipes/6030133.html',
        'http://www.recipage.com/recipes/6000759.html',
        'http://www.recipage.com/recipes/6024618.html',
        'http://www.recipage.com/recipes/6030965.html',
        'http://www.recipage.com/recipes/6004060.html',
        'http://www.recipage.com/recipes/6037953.html',
        'http://www.recipage.com/recipes/6019682.html',
        'http://www.recipage.com/recipes/6007413.html',
        'http://www.recipage.com/recipes/6036072.html',
        'http://www.recipage.com/recipes/6023553.html',
        'http://www.recipage.com/recipes/6000615.html',
        'http://www.recipage.com/recipes/6044208.html',
        'http://www.recipage.com/recipes/6001323.html',
        'http://www.recipage.com/recipes/6039246.html',
        'http://www.recipage.com/recipes/6043278.html',
        'http://www.recipage.com/recipes/6004858.html',
        'http://www.recipage.com/recipes/6005461.html',
        'http://www.recipage.com/recipes/6000757.html',
        'http://www.recipage.com/recipes/6001298.html',
        'http://www.recipage.com/recipes/6041108.html',
        'http://www.recipage.com/recipes/6030547.html',
        'http://www.recipage.com/recipes/6004338.html',
        'http://www.recipage.com/recipes/6005221.html',
        'http://www.recipage.com/recipes/6005066.html',
        'http://www.recipage.com/recipes/6006099.html',
        'http://www.recipage.com/recipes/6005354.html',
        'http://www.recipage.com/recipes/6035576.html',
        'http://www.recipage.com/recipes/6045198.html',
        'http://www.recipage.com/recipes/6000753.html',
        'http://www.recipage.com/recipes/6000617.html',
        'http://www.recipage.com/recipes/6004401.html',
        'http://www.recipage.com/recipes/6005006.html',
        'http://www.recipage.com/recipes/6001302.html',
        'http://www.recipage.com/recipes/6005505.html',
        'http://www.recipage.com/recipes/6004078.html',
        'http://www.recipage.com/recipes/6033228.html',
        'http://www.recipage.com/recipes/6045235.html',
        'http://www.recipage.com/recipes/6016515.html',
        'http://www.recipage.com/recipes/6001303.html',
        'http://www.recipage.com/recipes/6001228.html',
        'http://www.recipage.com/recipes/6002108.html',
        'http://www.recipage.com/recipes/6000756.html',
        'http://www.recipage.com/recipes/6027939.html',
        'http://www.recipage.com/recipes/6012962.html',
        'http://www.recipage.com/recipes/6007156.html',
        'http://www.recipage.com/recipes/6001002.html',
        'http://www.recipage.com/recipes/6001337.html',
        'http://www.recipage.com/recipes/6002107.html',
        'http://www.recipage.com/recipes/6006732.html',
        'http://www.recipage.com/recipes/6017111.html',
        'http://www.recipage.com/recipes/6014267.html',
        'http://www.recipage.com/recipes/6002109.html',
        'http://www.recipage.com/recipes/6001300.html',
        'http://www.recipage.com/recipes/6026089.html',
        'http://www.recipage.com/recipes/6000754.html',
        'http://www.recipage.com/recipes/6003959.html',
        'http://www.recipage.com/recipes/6004366.html',
        'http://www.recipage.com/recipes/6001325.html',
        'http://www.recipage.com/recipes/6035569.html',
        'http://www.recipage.com/recipes/6039634.html',
        'http://www.recipage.com/recipes/6017862.html',
        'http://www.recipage.com/recipes/6039396.html',
        'http://www.recipage.com/recipes/6033454.html',
        'http://www.recipage.com/recipes/6018581.html',
        'http://www.recipage.com/recipes/6025272.html',
        'http://www.recipage.com/recipes/6018582.html',
        'http://www.recipage.com/recipes/6002101.html',
        'http://www.recipage.com/recipes/6002243.html',
        'http://www.recipage.com/recipes/6002102.html',
        'http://www.recipage.com/recipes/6000750.html',
        'http://www.recipage.com/recipes/6040607.html',
        'http://www.recipage.com/recipes/6001242.html',
        'http://www.recipage.com/recipes/6030195.html',
        'http://www.recipage.com/recipes/6000752.html',
        'http://www.recipage.com/recipes/6042229.html',
        'http://www.recipage.com/recipes/6001332.html',
        'http://www.recipage.com/recipes/6038919.html',
        'http://www.recipage.com/recipes/6001322.html',
        'http://www.recipage.com/recipes/6030135.html',
        'http://www.recipage.com/recipes/6032274.html',
        'http://www.recipage.com/recipes/6006011.html',
        'http://www.recipage.com/recipes/6016398.html',
        'http://www.recipage.com/recipes/6002904.html',
        'http://www.recipage.com/recipes/6001223.html',
        'http://www.recipage.com/recipes/6045313.html',
        'http://www.recipage.com/recipes/6003509.html',
        'http://www.recipage.com/recipes/6001334.html',
        'http://www.recipage.com/recipes/6003988.html',
        'http://www.recipage.com/recipes/6011962.html',
        'http://www.recipage.com/recipes/6036101.html',
        'http://www.recipage.com/recipes/6000614.html',
        'http://www.recipage.com/recipes/6002264.html',
        'http://www.recipage.com/recipes/6019858.html',
        'http://www.recipage.com/recipes/6022752.html',
        'http://www.recipage.com/recipes/6026339.html',
        'http://www.recipage.com/recipes/6037949.html',
        'http://www.recipage.com/recipes/6002761.html',
        'http://www.recipage.com/recipes/6006093.html',
        'http://www.recipage.com/recipes/6002110.html',
        'http://www.recipage.com/recipes/6030542.html',
        'http://www.recipage.com/recipes/6001246.html',
        'http://www.recipage.com/recipes/6001245.html',
        'http://www.recipage.com/recipes/6029582.html',
        'http://www.recipage.com/recipes/6001328.html',
        'http://www.recipage.com/recipes/6028078.html',
        'http://www.recipage.com/recipes/6001336.html',
        'http://www.recipage.com/recipes/6001244.html',
        'http://www.recipage.com/recipes/6001320.html',
        'http://www.recipage.com/recipes/6000613.html',
        'http://www.recipage.com/recipes/6024479.html',
        'http://www.recipage.com/recipes/6001324.html',
        'http://www.recipage.com/recipes/6000612.html',
        'http://www.recipage.com/recipes/6014284.html',
        'http://www.recipage.com/recipes/6002716.html',
        'http://www.recipage.com/recipes/6019963.html',
        'http://www.recipage.com/recipes/6004969.html',
        'http://www.recipage.com/recipes/6036498.html',
        'http://www.recipage.com/recipes/6042732.html',
        'http://www.recipage.com/recipes/6030972.html',
        'http://www.recipage.com/recipes/6001227.html',
        'http://www.recipage.com/recipes/6006098.html',
        'http://www.recipage.com/recipes/6016197.html',
        'http://www.recipage.com/recipes/6002376.html',
        'http://www.recipage.com/recipes/6030548.html',
        'http://www.recipage.com/recipes/6021944.html',
        'http://www.recipage.com/recipes/6019211.html',
        'http://www.recipage.com/recipes/6006753.html',
        'http://www.recipage.com/recipes/6038352.html',
        'http://www.recipage.com/recipes/6001001.html',
        'http://www.recipage.com/recipes/6007176.html',
        'http://www.recipage.com/recipes/6018160.html',
        'http://www.recipage.com/recipes/6014855.html',
        'http://www.recipage.com/recipes/6029828.html',
        'http://www.recipage.com/recipes/6001304.html',
        'http://www.recipage.com/recipes/6029334.html',
        'http://www.recipage.com/recipes/6022880.html',
        'http://www.recipage.com/recipes/6006184.html',
        'http://www.recipage.com/recipes/6028910.html',
        'http://www.recipage.com/recipes/6004711.html',
        'http://www.recipage.com/recipes/6010774.html',
        'http://www.recipage.com/recipes/6031402.html',
        'http://www.recipage.com/recipes/6022543.html',
        'http://www.recipage.com/recipes/6025992.html',
        'http://www.recipage.com/recipes/6002114.html',
        'http://www.recipage.com/recipes/6033047.html',
        'http://www.recipage.com/recipes/6018029.html',
        'http://www.recipage.com/recipes/6001563.html',
        'http://www.recipage.com/recipes/6045237.html',
        'http://www.recipage.com/recipes/6013195.html',
        'http://www.recipage.com/recipes/6001239.html',
        'http://www.recipage.com/recipes/6038422.html',
        'http://www.recipage.com/recipes/6000747.html',
        'http://www.recipage.com/recipes/6000793.html',
        'http://www.recipage.com/recipes/6002898.html',
        'http://www.recipage.com/recipes/6004311.html',
        'http://www.recipage.com/recipes/6016658.html',
        'http://www.recipage.com/recipes/6031405.html',
        'http://www.recipage.com/recipes/6010166.html',
        'http://www.recipage.com/recipes/6019699.html',
        'http://www.recipage.com/recipes/6000792.html',
        'http://www.recipage.com/recipes/6021361.html',
        'http://www.recipage.com/recipes/6001299.html',
        'http://www.recipage.com/recipes/6026703.html',
        'http://www.recipage.com/recipes/6002258.html',
        'http://www.recipage.com/recipes/6012859.html',
        'http://www.recipage.com/recipes/6001308.html',
        'http://www.recipage.com/recipes/6000760.html',
        'http://www.recipage.com/recipes/6044641.html',
        'http://www.recipage.com/recipes/6031856.html',
        'http://www.recipage.com/recipes/6001241.html',
        'http://www.recipage.com/recipes/6021435.html',
        'http://www.recipage.com/recipes/6000791.html',
        'http://www.recipage.com/recipes/6000763.html',
        'http://www.recipage.com/recipes/6000762.html',
        'http://www.recipage.com/recipes/6004378.html',
        'http://www.recipage.com/recipes/6001240.html',
        'http://www.recipage.com/recipes/6001326.html',
        'http://www.recipage.com/recipes/6004361.html',
        'http://www.recipage.com/recipes/6030959.html',
        'http://www.recipage.com/recipes/6030551.html',
        'http://www.recipage.com/recipes/6004359.html',
        'http://www.recipage.com/recipes/6001309.html',
        'http://www.recipage.com/recipes/6001329.html',
        'http://www.recipage.com/recipes/6005292.html',
        'http://www.recipage.com/recipes/6007046.html',
        'http://www.recipage.com/recipes/6042719.html',
        'http://www.recipage.com/recipes/6042427.html',
        'http://www.recipage.com/recipes/6003888.html',
        'http://www.recipage.com/recipes/6010776.html',
        'http://www.recipage.com/recipes/6004272.html',
        'http://www.recipage.com/recipes/6005383.html',
        'http://www.recipage.com/recipes/6001305.html',
        'http://www.recipage.com/recipes/6001306.html',
        'http://www.recipage.com/recipes/6033967.html',
        'http://www.recipage.com/recipes/6001318.html',
        'http://www.recipage.com/recipes/6038022.html',
        'http://www.recipage.com/recipes/6045236.html',
        'http://www.recipage.com/recipes/6001321.html',
        'http://www.recipage.com/recipes/6030403.html',
        'http://www.recipage.com/recipes/6004790.html',
        'http://www.recipage.com/recipes/6027929.html',
        'http://www.recipage.com/recipes/6018423.html',
        'http://www.recipage.com/recipes/6004493.html',
        'http://www.recipage.com/recipes/6000751.html',
        'http://www.recipage.com/recipes/6005347.html',
        'http://www.recipage.com/recipes/6001333.html',
        'http://www.recipage.com/recipes/6002105.html',
        'http://www.recipage.com/recipes/6003717.html',
        'http://www.recipage.com/recipes/6005273.html',
        'http://www.recipage.com/recipes/6002982.html',
        'http://www.recipage.com/recipes/6001237.html',
        'http://www.recipage.com/recipes/6014982.html',
        'http://www.recipage.com/recipes/6000749.html',
        'http://www.recipage.com/recipes/6006761.html',
        'http://www.recipage.com/recipes/6000790.html',
        'http://www.recipage.com/recipes/6000788.html',
        'http://www.recipage.com/recipes/6000787.html',
        'http://www.recipage.com/recipes/6002112.html',
        'http://www.recipage.com/recipes/6000765.html',
        'http://www.recipage.com/recipes/6028893.html',
        'http://www.recipage.com/recipes/6045233.html',
        'http://www.recipage.com/recipes/6001335.html',
        'http://www.recipage.com/recipes/6007174.html',
        'http://www.recipage.com/recipes/6001307.html',
        'http://www.recipage.com/recipes/6044818.html',
        'http://www.recipage.com/recipes/6016611.html',
        'http://www.recipage.com/recipes/6002104.html',
        'http://www.recipage.com/recipes/6019824.html',
        'http://www.recipage.com/recipes/6021946.html',
        'http://www.recipage.com/recipes/6003001.html',
        'http://www.recipage.com/recipes/6002103.html',
        'http://www.recipage.com/recipes/6000761.html',
        'http://www.recipage.com/recipes/6000611.html',
        'http://www.recipage.com/recipes/6001000.html',
        'http://www.recipage.com/recipes/6028553.html',
        'http://www.recipage.com/recipes/6000758.html',
        'http://www.recipage.com/recipes/6035311.html',
        'http://www.recipage.com/recipes/6018756.html',
        'http://www.recipage.com/recipes/6041163.html',
        'http://www.recipage.com/recipes/6004090.html',
        'http://www.recipage.com/recipes/6037684.html',
        'http://www.recipage.com/recipes/6003038.html',
        'http://www.recipage.com/recipes/6001564.html',
        'http://www.recipage.com/recipes/6016249.html',
        'http://www.recipage.com/recipes/6013622.html',
        'http://www.recipage.com/recipes/6032270.html',
        'http://www.recipage.com/recipes/6004195.html',
        'http://www.recipage.com/recipes/6001243.html',
        'http://www.recipage.com/recipes/6004143.html',
        'http://www.recipage.com/recipes/6037799.html',
        'http://www.recipage.com/recipes/6009688.html',
        'http://www.recipage.com/recipes/6043807.html',
        'http://www.recipage.com/recipes/6028885.html',
        'http://www.recipage.com/recipes/6000789.html',
        'http://www.recipage.com/recipes/6000755.html',
        'http://www.recipage.com/recipes/6000764.html',
        'http://www.recipage.com/recipes/6001327.html',
        'http://www.recipage.com/recipes/6005314.html',
        'http://www.recipage.com/recipes/6005567.html',
        'http://www.recipage.com/recipes/6001319.html',
        'http://www.recipage.com/recipes/6044583.html',
        'http://www.recipage.com/recipes/6014854.html',
        'http://www.recipage.com/recipes/6004895.html',
        'http://www.recipage.com/recipes/6002106.html',
        'http://www.recipage.com/recipes/6000616.html',
        'http://www.recipage.com/recipes/6000748.html',
        'http://www.recipage.com/recipes/6017678.html',
        'http://www.recipage.com/recipes/6025072.html',
        'http://www.recipage.com/recipes/6007469.html',
        'http://www.recipage.com/recipes/6000999.html',
    ]

    def start_requests(self):
        requests = []
        for url in self.urls:
            request = self.make_requests_from_url(url)
            request.callback = self.parse_item
            requests.append(request)
        return requests
