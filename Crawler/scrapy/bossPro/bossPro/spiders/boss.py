import scrapy


class BossSpider(scrapy.Spider):
    name = 'boss'
    # allowed_domains = ['www.xxx.com']
    # start_urls = ['https://www.zhipin.com/job_detail/?query=python&city=101020100&industry=&position=']
    # 爬取前程无忧的招聘数据
    start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=']
    def parse_detail(self, response):
        # //text()表示拿到对应标签内的所有元素
        job_desc = response.xpath('/html/body/div[1]/div[2]/div[3]/div/div[2]/div[2]/div[1]/div//text()').extract()
        job_desc = ''.join(job_desc)
        print(job_desc)

    def parse(self, response):
        # li_list = response.xpath('/html/body/div[3]/div[3]/div/div[2]/div[4]/div[1]/div')
        li_list = response.xpath('/html/body')
        # li_list = response.xpath('body').extract_first()
        print(li_list)
        # print(li_list.count)
        # abc = []
        
        print(li_list.extract())
        return
        for li in li_list:
            job_name = li.xpath('./div/div[1]/div[1]/div/div[1]/span[1]/a/text()').extract_first()
            detail_url = li.xpath('./div/div[1]/div[1]/div/div[1]/span[1]/a/@href').extract_first()
            detail_url = 'https://www.zhipin.com/' + detail_url
            print(job_name)
            print(detail_url)

            yield scrapy.Request(detail_url,callback=self.parse_detail)
