import scrapy

class CpuSpider(scrapy.Spider):
    name = 'cpu_spider'
    start_urls = ['https://www.cpubenchmark.net/high_end_cpus.html']
    
    def parse_cpu_name(self, response):
        """Extract the CPU name using the CSS selector"""
        return response.css('span.cpuname::text').get().split(' @')[0]
    
    def parse_performance_cores(self, response):
        """Extracts and returns the number of cores of the CPU."""
        try:
            if response.css('p:contains("Performance Cores:")::text').get():
                return int(response.css('p:contains("Performance Cores:")::text').get().strip().split(", ")[0].split()[0])
            elif response.css('p:contains("Primary Cores:")::text').get():
                return int(response.css('p:contains("Primary Cores:")::text').get().strip().split(", ")[0].split()[0])
            else:
                return int(response.css('p.mobile-column::text').getall()[0].strip())
        except Exception:
            return 'N/A'

    def parse_performance_threads(self, response):
        """Extracts and returns the number of threads of the CPU."""
        try:
            if response.css('p:contains("Performance Cores:")::text').get():
                return int(response.css('p:contains("Performance Cores:")::text').get().strip().split(", ")[1].split()[0])
            elif response.css('p:contains("Primary Cores:")::text').get():
                return int(response.css('p:contains("Primary Cores:")::text').get().strip().split(", ")[1].split()[0])
            else:
                return int(response.css('p.mobile-column::text').getall()[1].strip())
        except Exception:
            return 'N/A'

    def parse_performance_clockspeed(self, response):
        """Extracts the clock speed of the performance cores of the CPU in GHz from the response."""
        try:
            if response.css('p:contains("Performance Cores:")::text').get():
                return float(response.css('p:contains("Performance Cores:")::text').get().strip().split(", ")[2].split()[0])
            elif response.css('p:contains("Primary Cores:")::text').get():
                return int(response.css('p:contains("Primary Cores:")::text').get().strip().split(", ")[2].split()[0])
            else:
                return float(response.css('p:contains("Clockspeed")::text').get().strip().split()[0])
        except Exception:
            return 'N/A'
    
    def parse_performance_turbospeed(self, response):
        """Extracts the turbo speed of the performance cores of the CPU in GHz from the response."""
        try:
            if response.css('p:contains("Performance Cores:")::text').get():
                return float(response.css('p:contains("Performance Cores:")::text').get().strip().split(", ")[3].split()[0])
            elif response.css('p:contains("Primary Cores:")::text').get():
                return int(response.css('p:contains("Primary Cores:")::text').get().strip().split(", ")[3].split()[0])
            else:
                return float(response.css('p:contains("Turbo Speed")::text').get().strip().split()[0])
        except Exception:
            return 'N/A'
        
    def parse_efficient_cores(self, response):
        """Extracts the number of efficient cores of the CPU from the response."""
        try:
            if response.css('p:contains("Efficient Cores:")::text').get():
                return int(response.css('p:contains("Efficient Cores:")::text').get().strip().split(": ")[0].split()[0])
            elif response.css('p:contains("Secondary Cores:")::text').get():
                return int(response.css('p:contains("Secondary Cores:")::text').get().strip().split(", ")[0].split()[0])
            else:
                return 'N/A'
        except Exception:
            return 'N/A'
        
    def parse_efficient_threads(self, response):
        """Extracts the number of efficient threads of the CPU from the response."""
        try:
            if response.css('p:contains("Efficient Cores:")::text').get():
                return int(response.css('p:contains("Efficient Cores:")::text').get().strip().split(", ")[1].split()[0])
            elif response.css('p:contains("Secondary Cores:")::text').get():
                return int(response.css('p:contains("Secondary Cores:")::text').get().strip().split(", ")[1].split()[0])
            else:
                return 'N/A'
        except Exception:
            return 'N/A'
        
    def parse_efficient_clockspeed(self, response):
        """Extracts the clock speed of the efficient cores of the CPU in GHz from the response."""
        try:
            if response.css('p:contains("Efficient Cores:")::text').get():
                return float(response.css('p:contains("Efficient Cores:")::text').get().strip().split(", ")[2].split()[0])
            elif response.css('p:contains("Secondary Cores:")::text').get():
                return int(response.css('p:contains("Secondary Cores:")::text').get().strip().split(", ")[2].split()[0])
            else:
                return 'N/A'
        except Exception:
            return 'N/A'

    def parse_efficient_turbospeed(self, response):
        """Extracts the turbo speed of the efficient cores of the CPU in GHz from the response."""
        try:
            if response.css('p:contains("Efficient Cores:")::text').get():
                return float(response.css('p:contains("Efficient Cores:")::text').get().strip().split(", ")[3].split()[0])
            elif response.css('p:contains("Secondary Cores:")::text').get():
                return int(response.css('p:contains("Secondary Cores:")::text').get().strip().split(", ")[3].split()[0])
            else:
                return 'N/A'
        except Exception:
            return 'N/A'
    
    def parse_tdp(self, response):
        """Extracts and returns the typical TDP (Thermal Design Power) of the CPU in watts."""
        try:
            return float(response.css('p:contains("Typical TDP")::text').get().strip().split()[0])
        except Exception:
            return 'N/A'
    
    def parse_multithread_rating(self, response):
        """Extracts and returns the multithread rating of the CPU."""
        try:
            return int(response.css('div:contains("Multithread Rating") + div[style*="font-weight: bold;"]::text').get().strip())
        except Exception:
            return 'N/A'
    
    def parse_single_thread_rating(self, response):
        """Extracts and returns the single thread rating of the CPU."""
        try:
            return int(response.css('div:contains("Single Thread Rating") + div[style*="font-weight: bold;"]::text').get().strip())
        except Exception:
            return 'N/A'

    def parse_L1_instruction_cache(self, response):
        """Extracts and returns the size of the L1 instruction cache."""
        try:
            return response.css('p:contains("Package")::text').getall()[0].strip().split(": ")[1]
        except Exception:
            return 'N/A'
    
    def parse_L1_data_cache(self, response):
        """Extracts and returns the size of the L1 data cache."""
        try:
            return response.css('p:contains("Package")::text').getall()[1].strip().split(": ")[1]
        except Exception:
            return 'N/A'
    
    def parse_L2_cache(self, response):
        """Extracts and returns the size of the L2 cache."""
        try:
            return response.css('p:contains("Package")::text').getall()[2].strip().split(": ")[1]
        except Exception:
            return 'N/A'
    
    def parse_L3_cache(self, response):
        """Extracts and returns the size of the L3 cache."""
        try:
            return response.css('p:contains("Package")::text').getall()[3].strip().split(": ")[1]
        except Exception:
            return 'N/A'
        
    def parse_eff_L1_instruction_cache(self, response):
        """Extracts and returns the size of the efficient L1 instruction cache."""
        try:
            return response.css('p:contains("Package")::text').getall()[4].strip().split(": ")[1]
        except Exception:
            return 'N/A'

    def parse_eff_L1_data_cache(self, response):
        """Extracts and returns the size of the efficient L1 data cache."""
        try:
            return response.css('p:contains("Package")::text').getall()[5].strip().split(": ")[1]
        except Exception:
            return 'N/A'
        
    def parse_eff_L2_cache(self, response):
        """Extracts and returns the size of the efficient L2 cache."""
        try:
            return response.css('p:contains("Package")::text').getall()[6].strip().split(": ")[1]
        except Exception:
            return 'N/A'
            
    def parse_integer_math(self, response):
        """Extracts and returns the integer math performance in MOps/Sec."""
        try:
            return int(response.css('table#test-suite-results td::text').getall()[0].split()[0].replace(",", ""))
        except Exception:
            return 'N/A'
    
    def parse_floating_point_math(self, response):
        """Extracts and returns the floating point math performance in MOps/Sec."""
        try:
            return int(response.css('table#test-suite-results td::text').getall()[1].split()[0].replace(",", ""))
        except Exception:
            return 'N/A'
    
    def parse_find_prime_numbers(self, response):
        """Extracts and returns the performance of finding prime numbers in Million Primes/Sec."""
        try:
            return int(response.css('table#test-suite-results td::text').getall()[2].split()[0].replace(",", ""))
        except Exception:
            return 'N/A'
    
    def parse_random_string_sorting(self, response):
        """Extracts and returns the performance of random string sorting in Thousand Primes/Sec."""
        try:
            return int(response.css('table#test-suite-results td::text').getall()[3].split()[0].replace(",", ""))
        except Exception:
            return 'N/A'
    
    def parse_data_encryption(self, response):
        """Extracts and returns the data encryption performance in MBytes/Sec."""
        try:
            return int(response.css('table#test-suite-results td::text').getall()[4].split()[0].replace(",", ""))
        except Exception:
            return 'N/A'
    
    def parse_data_compression(self, response):
        """Extracts and returns the data compression performance in KBytes/Sec."""
        try:
            return int(response.css('table#test-suite-results td::text').getall()[5].split()[0].replace(",", ""))
        except Exception:
            return 'N/A'
    
    def parse_physics(self, response):
        """Extracts and returns the physics performance in Frames/Sec."""
        try:
            return int(response.css('table#test-suite-results td::text').getall()[6].split()[0].replace(",", ""))
        except Exception:
            return 'N/A'
    
    def parse_extended_instructions(self, response):
        """Extracts and returns the performance of extended instructions in Million Matrices/Sec."""
        try:
            return int(response.css('table#test-suite-results td::text').getall()[7].split()[0].replace(",", ""))
        except Exception:
            return 'N/A'

    def parse_single_thread(self, response):
        """Extracts and returns the single thread performance in MOps/Sec."""
        try:
            return int(response.css('table#test-suite-results td::text').getall()[8].split()[0].replace(",", ""))
        except Exception:
            return 'N/A'

    def parse(self, response):
        cpu_requests = [response.follow(url=url, callback=self.parse_cpu) for url in response.css("ul.chartlist li a::attr(href)").getall()]
        for cpu_request in cpu_requests:
            yield cpu_request
            
    def parse_cpu(self, response):
        if "laptop" in response.css('div.left-desc-cpu p::text').get().strip().lower():
            yield {
                'name': self.parse_cpu_name(response),
                'performance_clockspeed': self.parse_performance_clockspeed(response),
                'performance_turbospeed': self.parse_performance_turbospeed(response),
                'performance_cores': self.parse_performance_cores(response),
                'performance_threads': self.parse_performance_threads(response),
                'efficient_clockspeed': self.parse_efficient_clockspeed(response),
                'efficient_turbospeed': self.parse_efficient_turbospeed(response),
                'efficient_cores': self.parse_efficient_cores(response),
                'efficient_threads': self.parse_efficient_threads(response),
                'tdp': self.parse_tdp(response),
                'multithread_rating': self.parse_multithread_rating(response),
                'single_thread_rating': self.parse_single_thread_rating(response),
                'L1_instruction_cache': self.parse_L1_instruction_cache(response),
                'L1_data_cache': self.parse_L1_data_cache(response),
                'L2_cache': self.parse_L2_cache(response),
                'L3_cache': self.parse_L3_cache(response),
                'eff_L1_instruction_cache': self.parse_eff_L1_instruction_cache(response),
                'eff_L1_data_cache': self.parse_eff_L1_data_cache(response),
                'eff_L2_cache': self.parse_eff_L2_cache(response),
                'integer_math': self.parse_integer_math(response),
                'floating_point_math': self.parse_floating_point_math(response),
                'find_prime_numbers': self.parse_find_prime_numbers(response),
                'random_string_sorting': self.parse_random_string_sorting(response),
                'data_encryption': self.parse_data_encryption(response),
                'data_compression': self.parse_data_compression(response),
                'physics': self.parse_physics(response),
                'extended_instructions': self.parse_extended_instructions(response),
                'single_thread': self.parse_single_thread(response)
            }
        else:
            pass