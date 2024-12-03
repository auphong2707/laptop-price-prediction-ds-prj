import scrapy

class GPUSpider(scrapy.Spider):
    """Sponsor by Peter Parker"""
    name = 'gpu_spider'
    start_urls = ['https://www.videocardbenchmark.net/high_end_gpus.html',
                  'https://www.videocardbenchmark.net/mid_range_gpus.html', 
                  'https://www.videocardbenchmark.net/midlow_range_gpus.html',
                  'https://www.videocardbenchmark.net/low_end_gpus.html']

    def parse_gpu_name(self, response):
        """Extract the GPU name using the CSS selector"""
        name = response.css('span.cpuname::text').get().strip().lower()
        for removal in ["laptop gpu", "(mobile)"]:
            name = name.replace(removal, "")
        return name.strip()
    
    def parse_avg_g3d_mark(self, response):
        """Extract the GPU average G3D mark using the CSS selector"""
        try:
            return int(response.css("div.right-desc span[style*='font-size: 44px']::text").get())
        except Exception:
            return "n/a"
    
    def parse_gpu_bus_interface(self, response):
        """Extract the GPU bus using the CSS selector"""
        try:
            return response.css('p:contains("Bus Interface:")::text').get().strip().lower()
        except Exception:
            return 'n/a'
        
    def parse_gpu_max_memory_size(self, response):
        """Extract the GPU max memory size in MB using the CSS selector"""
        try:
            return int(response.css('p:contains("Max Memory Size:")::text').get().strip().split(", ")[0].split()[0])
        except Exception:
            return "n/a"

    def parse_gpu_core_clock(self, response):
        """Extract the GPU core clock in Mhz using the CSS selector"""
        try:
            return int(response.css('p:contains("Core Clock(s):")::text').get().strip().split(", ")[0].split()[0])
        except Exception:
            return "n/a"
    
    def parse_gpu_max_directx(self, response):
        """Extract the GPU max compatible direct X version using the CSS selector"""
        try:
            return response.css('p:contains("DirectX:")::text').get().strip().split(", ")[0].split()[0].lower()
        except Exception:
            return "n/a"
    
    def parse_gpu_open_gl(self, response):
        """Extract the GPU open GL using the CSS selector"""
        try:
            return float(response.css('p:contains("OpenGL:")::text').get().strip().split(", ")[0].split()[0])
        except Exception:
            return "n/a"
    
    def parse_gpu_max_tdp(self, response):
        """Extract the GPU max TDP in W using the CSS selector"""
        try:
            return int(response.css('p:contains("Max TDP")::text').get().strip().split(", ")[0].split()[0])
        except Exception:
            return 'n/a'
        
    def parse_test_directx_9(self, response):
        """Extract the test results of DirectX 9 in Frames/Sec using CSS selector"""
        try:
            return int(response.css('#test-suite-results th:contains("DirectX 9") + td::text').get().strip().split(", ")[0].split()[0])
        except Exception:
            return "n/a"

    def parse_test_directx_10(self, response):
        """Extract the test results of DirectX 10 in Frames/Sec using CSS selector"""
        try:
            return int(response.css('#test-suite-results th:contains("DirectX 10") + td::text').get().strip().split(", ")[0].split()[0])
        except Exception:
            return "n/a"
    
    def parse_test_directx_11(self, response):
        """Extract the test results of DirectX 11 in Frames/Sec using CSS selector"""
        try:
            return int(response.css('#test-suite-results th:contains("DirectX 11") + td::text').get().strip().split(", ")[0].split()[0])
        except Exception:
            return "n/a"
    
    def parse_test_directx_12(self, response):
        """Extract the test results of DirectX 12 in Frames/Sec using CSS selector"""
        try:
            return int(response.css('#test-suite-results th:contains("DirectX 12") + td::text').get().strip().split(", ")[0].split()[0])
        except Exception:
            return "n/a"
    
    def parse_test_gpu_compute(self, response):
        """Extract the test results of GPU compute in Ops/Sec using CSS selector"""
        try:
            return int(response.css('#test-suite-results th:contains("GPU Compute") + td::text').get().strip().split(", ")[0].split()[0])
        except Exception:
            return "n/a"
    
    def parse(self, response):
        gpu_requests = [response.follow(url=url, callback=self.parse_gpu) for url in response.css("ul.chartlist li a::attr(href)").getall()]
        for gpu_request in gpu_requests:
            yield gpu_request

    def parse_gpu(self, response):
        if "laptop gpu" in response.css('span.cpuname::text').get().strip().lower() \
            or (response.css('p:contains("Videocard Category:")::text').get() is not None \
                and response.css('p:contains("Videocard Category:")::text').get().strip() == 'Mobile') \
            or "geforce mx" in self.parse_gpu_name(response):
                yield {
                    'name': self.parse_gpu_name(response),
                    'avg_g3d_mark': self.parse_avg_g3d_mark(response),
                    'bus_interface': self.parse_gpu_bus_interface(response),
                    'max_memory_size': self.parse_gpu_max_memory_size(response),
                    'core_clock': self.parse_gpu_core_clock(response),
                    'max_direct': self.parse_gpu_max_directx(response),
                    'open_gl': self.parse_gpu_open_gl(response),
                    'max_tdp': self.parse_gpu_max_tdp(response),
                    'test_directx_9': self.parse_test_directx_9(response),
                    'test_directx_10': self.parse_test_directx_10(response),
                    'test_directx_11': self.parse_test_directx_11(response),
                    'test_directx_12': self.parse_test_directx_12(response),
                    'test_gpu_compute': self.parse_test_gpu_compute(response)
                }
