"""
Earnings Data Fetcher Agent
Fetches earnings calendar and transcripts (currently using mock data)
"""

import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class EarningsFetcher:
    """
    Fetches earnings calendar and transcript data.
    Currently uses mock data - will integrate real APIs later.
    """

    def __init__(self, cache_dir: str = "data"):
        """
        Initialize earnings fetcher.

        Args:
            cache_dir: Directory to cache earnings data
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.cache_file = os.path.join(cache_dir, "earnings_cache.json")
        logger.info("EarningsFetcher initialized")

    def get_earnings_calendar(self, days_ahead: int = 30) -> List[Dict]:
        """
        Get upcoming earnings dates.

        Args:
            days_ahead: Number of days to look ahead

        Returns:
            List of dicts with ticker, company, date, and time

        TODO: Integrate real earnings calendar API:
        - Alpha Vantage EARNINGS_CALENDAR endpoint
        - Financial Modeling Prep API
        - Yahoo Finance earnings calendar scraper
        """
        logger.info(f"Fetching earnings calendar for next {days_ahead} days")

        # Mock data - realistic upcoming earnings dates
        today = datetime.now()
        mock_calendar = [
            {
                "ticker": "AAPL",
                "company": "Apple Inc.",
                "sector": "Technology",
                "date": (today + timedelta(days=7)).strftime("%Y-%m-%d"),
                "time": "After Market Close",
                "quarter": "Q1 2025",
                "fiscal_year": 2025,
                "estimated_eps": 2.10,
                "estimated_revenue": 118.5e9
            },
            {
                "ticker": "MSFT",
                "company": "Microsoft Corporation",
                "sector": "Technology",
                "date": (today + timedelta(days=12)).strftime("%Y-%m-%d"),
                "time": "After Market Close",
                "quarter": "Q2 2025",
                "fiscal_year": 2025,
                "estimated_eps": 2.75,
                "estimated_revenue": 60.2e9
            },
            {
                "ticker": "NVDA",
                "company": "NVIDIA Corporation",
                "sector": "Technology",
                "date": (today + timedelta(days=18)).strftime("%Y-%m-%d"),
                "time": "After Market Close",
                "quarter": "Q4 2024",
                "fiscal_year": 2024,
                "estimated_eps": 5.15,
                "estimated_revenue": 20.8e9
            },
            {
                "ticker": "JPM",
                "company": "JPMorgan Chase & Co.",
                "sector": "Financials",
                "date": (today + timedelta(days=5)).strftime("%Y-%m-%d"),
                "time": "Before Market Open",
                "quarter": "Q1 2025",
                "fiscal_year": 2025,
                "estimated_eps": 4.25,
                "estimated_revenue": 41.2e9
            },
            {
                "ticker": "JNJ",
                "company": "Johnson & Johnson",
                "sector": "Healthcare",
                "date": (today + timedelta(days=22)).strftime("%Y-%m-%d"),
                "time": "Before Market Open",
                "quarter": "Q1 2025",
                "fiscal_year": 2025,
                "estimated_eps": 2.65,
                "estimated_revenue": 24.8e9
            }
        ]

        # Save to cache
        self._save_to_cache({"earnings_calendar": mock_calendar, "fetched_at": datetime.now().isoformat()})

        logger.info(f"Retrieved {len(mock_calendar)} upcoming earnings events")
        return mock_calendar

    def get_earnings_transcript(self, ticker: str) -> Optional[Dict]:
        """
        Get earnings call transcript for a ticker.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dict with transcript text and metadata, or None if not found

        TODO: Integrate real transcript sources:
        - Alpha Vantage NEWS_SENTIMENT endpoint for earnings context
        - SEC EDGAR 8-K filings parser
        - Seeking Alpha transcripts API
        - Financial Modeling Prep transcripts
        """
        ticker = ticker.upper()
        logger.info(f"Fetching earnings transcript for {ticker}")

        # Mock transcripts - realistic financial language (50 companies total)
        # Sentiment distribution: 60% positive, 30% neutral, 10% negative
        mock_transcripts = {
            # POSITIVE SENTIMENT (30 companies - 60%)
            "AAPL": {
                "ticker": "AAPL",
                "company": "Apple Inc.",
                "date": "2025-10-28",
                "quarter": "Q4 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good afternoon and thank you for joining us. Today we're reporting record quarterly
                revenue of $89.5 billion, up 6% year over year, driven by strong iPhone 15 demand
                and continued services growth. Our installed base of active devices reached a new
                all-time high across all major product categories and geographic segments.

                iPhone revenue was $43.8 billion, up 3% despite a challenging comparison to last year's
                iPhone 14 launch. We're seeing exceptional demand for iPhone 15 Pro models, with customers
                valuing the advanced camera system and A17 Pro chip performance. Customer satisfaction
                ratings remain at industry-leading levels of 98%.

                Services revenue hit a new record of $22.3 billion, up 16% year over year. This growth
                reflects the strength of our ecosystem and increasing customer engagement across App Store,
                Apple Music, iCloud, and Apple TV+. Our Services gross margin expanded to 72%, demonstrating
                the leverage in this high-margin business. We continue to invest heavily in AI capabilities
                that will drive the next wave of innovation across our product lineup.
                """
            },
            "MSFT": {
                "ticker": "MSFT",
                "company": "Microsoft Corporation",
                "date": "2025-10-24",
                "quarter": "Q1 2025",
                "fiscal_year": 2025,
                "transcript": """
                Thank you for joining us today. We delivered strong results with revenue of $56.5 billion,
                up 13% year over year, and operating income of $26.9 billion, up 25%. Our Intelligent
                Cloud segment continues to be the primary growth driver, powered by Azure's 29% growth
                in constant currency.

                Azure AI services saw unprecedented demand, with AI-related revenue growing triple digits.
                Over 18,000 organizations are now using Azure OpenAI Service, up from 11,000 last quarter.
                We're seeing strong adoption across industries including healthcare, financial services,
                and manufacturing. Our Copilot products have reached 1 million paid users faster than
                any enterprise product in our history.

                Productivity and Business Processes revenue was $18.6 billion, up 13%, with Microsoft 365
                commercial seats growing 11%. We're seeing healthy trends in both new customer acquisition
                and existing customer expansion. Our gaming business contributed $4.8 billion in revenue,
                with Xbox Game Pass subscribers reaching 34 million. We remain confident in our long-term
                growth trajectory and are raising our full-year guidance across all segments.
                """
            },
            "NVDA": {
                "ticker": "NVDA",
                "company": "NVIDIA Corporation",
                "date": "2025-10-20",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good afternoon everyone. We're pleased to report exceptional third quarter results with
                record revenue of $18.1 billion, up 206% year over year and up 34% sequentially. Data
                Center revenue reached a record $14.5 billion, up 279% year over year, driven by surging
                demand for our Hopper architecture GPUs.

                Demand for our AI computing platforms significantly exceeds supply, and we expect this
                dynamic to continue into next year. Major cloud service providers, consumer internet
                companies, and enterprises are racing to deploy generative AI capabilities. We shipped
                over 100,000 H100 GPUs this quarter and are ramping production aggressively to meet
                unprecedented demand.

                Our Gaming segment delivered solid results with revenue of $2.9 billion, up 15% sequentially,
                benefiting from strong demand for RTX 40-series GPUs. Professional Visualization revenue
                was $0.4 billion, showing signs of stabilization after several quarters of decline. Gross
                margins expanded to 75%, reflecting favorable product mix toward higher-margin Data Center
                products. We're introducing next-generation B100 GPUs in early 2025 which will further
                extend our technology leadership in AI training and inference.
                """
            },
            "META": {
                "ticker": "META",
                "company": "Meta Platforms Inc.",
                "date": "2025-10-25",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good afternoon. We delivered outstanding third quarter results with revenue of $34.1 billion,
                up 23% year over year, significantly exceeding expectations. Our family of apps continues
                to see strong engagement growth, with over 3.14 billion daily active people across Facebook,
                Instagram, WhatsApp, and Threads. Advertising revenue grew 24% as our AI-powered ad products
                drive better ROI for advertisers.

                We're seeing exceptional results from our Advantage+ suite, which uses AI to optimize ad
                creative, targeting, and placement. Adoption has exceeded our expectations with over 1 million
                advertisers now using these tools. Click-through rates have improved 12% and conversion costs
                have declined 8% for advertisers using our AI recommendations. Our Reality Labs segment showed
                progress with Quest 3 exceeding sales targets and strong developer momentum for our mixed
                reality platform. We're raising our full-year revenue guidance to $134-137 billion and
                increasing our investment in AI infrastructure to maintain our competitive advantage.
                """
            },
            "AMZN": {
                "ticker": "AMZN",
                "company": "Amazon.com Inc.",
                "date": "2025-10-26",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Thank you for joining. Amazon delivered exceptional third quarter performance with net sales
                of $143.1 billion, up 13% year over year, and operating income of $11.2 billion, more than
                doubling versus last year. AWS revenue grew 12% to $23.1 billion with accelerating growth
                as enterprises increase cloud adoption. We're seeing particularly strong demand for our
                generative AI services with thousands of customers building on Amazon Bedrock.

                North America segment operating margin expanded to 5.9%, our highest level in over two years,
                driven by improved fulfillment productivity and better inventory management. Prime Day was
                our biggest event ever with record member participation. Our advertising business grew 26%
                to $12.1 billion as we continue to innovate with sponsored products and streaming ads. We
                recently announced our NFL Thursday Night Football partnership is delivering 50% higher
                viewership than broadcast alternatives. Based on our strong performance and momentum heading
                into the holiday season, we're raising guidance for Q4 revenue to $160-167 billion.
                """
            },
            "GOOGL": {
                "ticker": "GOOGL",
                "company": "Alphabet Inc.",
                "date": "2025-10-24",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good afternoon everyone. Alphabet delivered strong third quarter results with revenues of
                $76.7 billion, up 11% year over year, and operating margin expansion to 28%. Google Search
                and other advertising revenues were $44.0 billion, up 11%, with continued strength in retail
                vertical and growing adoption of Performance Max campaigns that leverage our AI capabilities.

                YouTube advertising revenue reached $7.9 billion, up 12%, with Shorts now averaging over
                70 billion daily views. YouTube TV surpassed 6 million subscribers, making it the fastest
                growing TV service in the US. Google Cloud revenue grew 22% to $8.4 billion with operating
                margin turning positive at 3%, a significant milestone demonstrating the operating leverage
                in this business. We're seeing strong customer wins in retail, financial services, and
                healthcare sectors. Our Bard AI assistant has been integrated across our product portfolio
                and we're excited about the opportunities ahead. We're raising our full-year capex guidance
                to support continued AI infrastructure buildout.
                """
            },
            "TSLA": {
                "ticker": "TSLA",
                "company": "Tesla Inc.",
                "date": "2025-10-18",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Thank you for joining our Q3 earnings call. Tesla achieved record quarterly deliveries of
                435,000 vehicles, up 27% year over year, with production exceeding 440,000 vehicles. Revenue
                reached $23.4 billion with automotive gross margin improving to 19.8% despite competitive
                pricing. Model Y remains the best-selling vehicle globally and demand for Cybertruck continues
                to exceed our production capacity with over 1.5 million reservations.

                Our energy storage deployments reached a record 4.0 GWh, more than doubling year over year
                as utilities and commercial customers accelerate grid storage adoption. Megapack production
                at our dedicated Nevada facility is ramping rapidly. Full Self-Driving beta has now been
                released to over 400,000 customers with safety metrics showing significant improvement.
                Our AI training infrastructure continues to expand with Dojo supercomputer now operational.
                We're on track to begin Cybertruck deliveries next month and production of our next-generation
                platform in 2025. We expect to achieve 1.8 million vehicle deliveries for the full year.
                """
            },
            "V": {
                "ticker": "V",
                "company": "Visa Inc.",
                "date": "2025-10-23",
                "quarter": "Q4 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good afternoon. Visa delivered exceptional fourth quarter results with net revenues of
                $8.6 billion, up 11% year over year in constant dollars. Payments volume grew 8% to
                $3.3 trillion and processed transactions increased 10% to 56.2 billion, demonstrating
                the continued shift to digital payments globally. Cross-border volume excluding intra-Europe
                grew 17%, benefiting from strong travel recovery and e-commerce growth.

                Our value-added services revenue grew 20%, driven by strong adoption of fraud and identity
                solutions, Visa Direct, and our acceptance solutions. Visa Direct transactions reached
                2.1 billion in the quarter, up 32%, as we expand into new use cases including disbursements,
                payouts, and peer-to-peer payments. We're seeing excellent traction with our new credentials
                including digital wallets and tokenized commerce. Client incentives as a percentage of gross
                revenues improved 20 basis points as we optimize our investments. We're raising our full-year
                FY25 net revenue growth guidance to low double-digits reflecting strong momentum.
                """
            },
            "MA": {
                "ticker": "MA",
                "company": "Mastercard Inc.",
                "date": "2025-10-25",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Thank you for joining us. Mastercard reported strong third quarter results with net revenue
                of $6.5 billion, up 13% year over year, and EPS of $3.39, up 17%. Gross dollar volume
                increased 11% to $2.4 trillion with cross-border volume up 17%, exceeding pre-pandemic
                levels. Switched transactions grew 14% to 36.8 billion, reflecting healthy consumer spending
                and continued digitalization of payments globally.

                Our services offerings continued exceptional growth with revenue up 18%, driven by cyber
                and intelligence solutions, data analytics, and consulting. We're seeing strong demand for
                our fraud detection and prevention capabilities as digital commerce expands. Open banking
                solutions gained traction with major bank partnerships in Europe and Latin America. Our
                Send platform for real-time disbursements processed over 950 million transactions, up 40%.
                We recently announced strategic partnerships with major fintechs to expand acceptance in
                emerging markets. Based on our strong performance and positive trends, we're raising our
                full-year revenue growth guidance to the high end of our 11-13% range.
                """
            },
            "CRM": {
                "ticker": "CRM",
                "company": "Salesforce Inc.",
                "date": "2025-10-27",
                "quarter": "Q3 2025",
                "fiscal_year": 2025,
                "transcript": """
                Good afternoon. Salesforce delivered outstanding third quarter results with revenue of
                $8.7 billion, up 11% year over year, and operating margin of 30.5%, expanding 470 basis
                points. Our Einstein GPT and AI Cloud offerings are resonating strongly with customers,
                with over 4,000 companies now implementing our generative AI solutions. Revenue from AI
                products exceeded expectations and is becoming a meaningful contributor to growth.

                Current remaining performance obligation grew 13% to $49.1 billion, indicating strong
                future revenue visibility. We signed several landmark deals this quarter including expanded
                enterprise agreements with major retailers and financial institutions. Customer 360 adoption
                continues to accelerate with organizations consolidating onto our platform. Tableau and
                MuleSoft integration is delivering synergies ahead of schedule. Our focus on profitable
                growth is evident in our margin performance while maintaining industry-leading innovation.
                We're raising our full-year revenue guidance to $34.7-34.8 billion and operating margin
                guidance to 30.5%, reflecting confidence in our execution and market opportunity.
                """
            },
            "ADBE": {
                "ticker": "ADBE",
                "company": "Adobe Inc.",
                "date": "2025-10-15",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Thank you for joining Adobe's Q3 earnings call. We delivered record revenue of $4.89 billion,
                up 10% year over year, with Digital Media revenue of $3.59 billion, up 11%. Creative Cloud
                revenue grew 11% to $3.02 billion driven by strong demand for our Firefly generative AI
                capabilities integrated across our creative applications. Over 3 billion images have been
                generated using Firefly since launch, with enterprise adoption accelerating.

                Document Cloud revenue reached $625 million, up 18%, as digital document workflows continue
                to displace paper-based processes. Acrobat AI Assistant is seeing excellent early traction
                with strong conversion rates from free trials. Our Experience Cloud delivered $1.15 billion
                in revenue with healthy new customer acquisition and existing customer expansion. Operating
                margin expanded to 37.2% reflecting disciplined expense management and operating leverage.
                Based on our strong performance and product momentum, particularly around AI innovation,
                we're raising our full-year revenue target to $19.4 billion and expect to exit the year
                with accelerating growth momentum into fiscal 2025.
                """
            },
            "QCOM": {
                "ticker": "QCOM",
                "company": "Qualcomm Inc.",
                "date": "2025-10-19",
                "quarter": "Q4 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good afternoon and thank you for joining us. Qualcomm reported strong fourth quarter results
                with revenue of $9.9 billion, up 13% year over year, exceeding the high end of guidance.
                QCT revenue was $8.7 billion with handset chipset revenue up 16% as premium tier Android
                devices gained share. Our Snapdragon 8 Gen 3 is ramping with excellent customer reception
                and design wins across all major OEMs globally.

                Automotive revenue reached $560 million, up 25%, with our design win pipeline now exceeding
                $30 billion. We're expanding beyond infotainment into advanced driver assistance and digital
                cockpit solutions. IoT revenue of $1.5 billion grew 8% driven by edge networking and industrial
                applications. QTL licensing revenue was $1.2 billion with strong 5G device ramp in China and
                emerging markets. Our AI initiatives are gaining momentum with on-device AI capabilities
                becoming a key differentiator for our Snapdragon platforms. We're providing Q1 guidance above
                consensus and raising our long-term automotive revenue target to $4 billion by 2026, reflecting
                our strong competitive position.
                """
            },
            "UNH": {
                "ticker": "UNH",
                "company": "UnitedHealth Group Inc.",
                "date": "2025-10-13",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good morning. UnitedHealth Group delivered strong third quarter performance with revenues
                of $92.4 billion, up 14% year over year, and adjusted earnings per share of $6.56, up 11%.
                UnitedHealthcare served 53.1 million people, adding 1.8 million members over the past year
                with growth across all major businesses. Our Medicare Advantage membership grew 8% with
                strong retention and positive member experience scores.

                Optum Health revenue grew 27% to $24.3 billion with patients served increasing to 103 million.
                Our value-based care arrangements now cover over 5 million patients with demonstrated quality
                improvements and cost savings. Optum Rx processed 360 million adjusted scripts in the quarter
                with good retention of large employer clients. Operating cost ratio improved 60 basis points
                reflecting our continued focus on efficiency and care quality. We're raising our full-year
                adjusted EPS guidance to $24.85-25.00, up from our prior range, based on strong operational
                performance across all business segments and confidence in our Medicare Advantage position
                heading into Annual Enrollment Period.
                """
            },
            "PFE": {
                "ticker": "PFE",
                "company": "Pfizer Inc.",
                "date": "2025-10-27",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good morning everyone. Pfizer reported third quarter revenues of $17.2 billion with
                operational revenue growth excluding COVID products of 14%. Our in-line products portfolio
                delivered strong performance with Eliquis revenue up 9% to $1.8 billion and Vyndaqel franchise
                growing 64% to $1.1 billion as cardiologist adoption accelerates for transthyretin amyloid
                cardiomyopathy treatment.

                Our newly launched products are exceeding expectations with Abrysvo RSV vaccine achieving
                $515 million in revenue as we enter the respiratory season. Velsipity for ulcerative colitis
                is ramping well with strong formulary coverage. Seagen acquisition integration is ahead of
                schedule with four antibody-drug conjugates now generating combined revenue exceeding $2 billion
                annually. Our oncology pipeline strengthened with positive Phase 3 data for our CDK4/6 inhibitor
                and breakthrough therapy designation for our lung cancer asset. We're raising full-year revenue
                guidance to $58.5-61.5 billion and reaffirming our confidence in achieving mid-single digit
                CAGR through 2030 as we transition from COVID dependence to sustainable growth.
                """
            },
            "ABBV": {
                "ticker": "ABBV",
                "company": "AbbVie Inc.",
                "date": "2025-10-25",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Thank you for joining our third quarter earnings call. AbbVie delivered strong results with
                net revenues of $14.5 billion, up 4% operationally, and adjusted EPS of $3.05, up 5%.
                Our immunology portfolio excluding Humira grew 22% with Skyrizi revenue reaching $2.7 billion
                and Rinvoq $1.3 billion. We received FDA approvals for four new indications this quarter,
                expanding our addressable market significantly.

                Aesthetics revenue grew 6% to $1.3 billion with Botox Cosmetic up 8% driven by strong patient
                demand and successful marketing campaigns. Neuroscience revenue was $4.1 billion with Vraylar
                maintaining leadership in bipolar depression and schizophrenia. Our oncology portfolio
                delivered $1.7 billion with Venclexta franchise up 13%. Importantly, our pipeline advanced
                with positive Phase 3 results for our oral IL-23 inhibitor and our next-generation JAK
                inhibitor. We're managing the Humira biosimilar transition better than expected with our
                new growth drivers offsetting the decline. We're raising our full-year adjusted EPS guidance
                to $11.13-11.17, reflecting confidence in our diversified portfolio and pipeline momentum.
                """
            },
            "TMO": {
                "ticker": "TMO",
                "company": "Thermo Fisher Scientific Inc.",
                "date": "2025-10-23",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good morning. Thermo Fisher delivered excellent third quarter performance with revenue of
                $10.6 billion, up 4% organically, and adjusted EPS of $5.25, exceeding expectations. Our
                Life Sciences Solutions segment grew 6% with strong demand for bioprocess equipment and
                bioproduction consumables as cell and gene therapy programs advance from clinical to
                commercial scale.

                Analytical Instruments revenue increased 5% with particular strength in electron microscopy
                and mass spectrometry for semiconductor and materials science applications. Our Specialty
                Diagnostics business grew 8% driven by allergy and autoimmune testing expansion. Laboratory
                Products and Biopharma Services segment delivered solid performance with pharma services
                revenue up 9% as our CDMO capabilities see robust demand. We announced strategic acquisitions
                in the spatial biology and single-cell analysis markets to strengthen our genomics portfolio.
                Our Practical Process Improvement initiatives delivered $130 million in savings this quarter.
                Based on strong execution and improving market conditions, we're raising our full-year revenue
                guidance to $42.4 billion and adjusted EPS to $21.13-21.33.
                """
            },
            "WMT": {
                "ticker": "WMT",
                "company": "Walmart Inc.",
                "date": "2025-10-19",
                "quarter": "Q3 2025",
                "fiscal_year": 2025,
                "transcript": """
                Good morning. Walmart delivered outstanding third quarter results with total revenue of
                $160.8 billion, up 5.5% year over year, and comp sales growth of 5.3% in the US. We're
                gaining market share across income cohorts and merchandise categories as customers choose
                Walmart for value, convenience, and quality. Grocery comp sales were particularly strong
                with sustained unit growth and improved fresh food sales.

                E-commerce sales grew 27% with store-fulfilled pickup and delivery continuing rapid adoption.
                Our membership programs now exceed 38 million households globally with retention rates
                improving. Walmart+ members spend 2.5x more than non-members and shop 3x more frequently.
                Operating income grew 8.2% to $6.7 billion with operating margin expanding 10 basis points
                despite inflation pressures, demonstrating our expense discipline. International delivered
                strong results with Walmex and Flipkart both posting double-digit growth. We're raising our
                full-year comp sales guidance to 4.0-4.5% and EPS guidance to $6.40-6.48, reflecting our
                strong competitive position and operational execution.
                """
            },
            "HD": {
                "ticker": "HD",
                "company": "The Home Depot Inc.",
                "date": "2025-10-17",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Thank you for joining. The Home Depot reported strong third quarter results with sales of
                $37.7 billion and comparable sales growth of 3.1%, our best performance in six quarters.
                Pro customer sales outpaced DIY with our Pro ecosystem delivering double-digit growth as
                contractors increase engagement with our platform. Big ticket transactions over $1,000
                increased 4.2%, indicating healthy project activity.

                Gross margin expanded 35 basis points to 33.6% driven by favorable product mix, lower
                shrink, and effective promotional management. Our supply chain investments are paying off
                with improved in-stock positions and faster delivery times. Digital sales grew 7% and
                represented 14.5% of total sales with strong momentum in our mobile app. Our interconnected
                shopping experience is resonating with customers buying online and picking up in store
                growing double-digits. Operating margin expanded to 14.8% as productivity gains offset wage
                investments. Based on our strong Q3 performance and improving market indicators, we're
                raising our full-year comparable sales guidance to positive 2-3% and expect operating margin
                expansion for the full year.
                """
            },
            "MCD": {
                "ticker": "MCD",
                "company": "McDonald's Corporation",
                "date": "2025-10-24",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good morning everyone. McDonald's delivered strong third quarter results with global comparable
                sales up 9.0%, exceeding expectations. US comp sales increased 8.1% driven by strategic menu
                pricing, digital channel growth, and successful marketing campaigns. Our MyMcDonald's Rewards
                program now has over 150 million active members globally, up from 110 million a year ago,
                driving higher visit frequency and check size.

                International Operated Markets posted 8.3% comp growth with particularly strong performance
                in the UK, Germany, and Canada. International Developmental Licensed Markets grew 10.5% with
                robust growth in Japan and Latin America. Digital channels accounted for over $7 billion in
                systemwide sales this quarter, representing nearly 40% of total sales in our top markets.
                Our loyalty members visit 50% more frequently and spend 30% more per visit than non-members.
                Restaurant margin expanded 200 basis points to 19.2% reflecting pricing power and operational
                improvements. We're raising our full-year growth outlook and remain confident in achieving
                our long-term targets of 4-5% annual comp growth.
                """
            },
            "NKE": {
                "ticker": "NKE",
                "company": "Nike Inc.",
                "date": "2025-10-21",
                "quarter": "Q1 2025",
                "fiscal_year": 2025,
                "transcript": """
                Good afternoon. Nike delivered excellent first quarter results with revenues of $12.9 billion,
                up 8% on a currency-neutral basis, and gross margin expansion of 140 basis points to 44.3%.
                Our Direct business grew 17% and now represents 44% of total Nike Brand revenue, up from
                39% last year. Digital commerce was particularly strong, up 25%, as our apps and member
                ecosystem drive deeper engagement.

                Nike Brand footwear revenue grew 9% with strong demand across all categories particularly
                running, basketball, and sportswear. Jordan Brand delivered another record quarter with
                revenue up 15%. Our Women's business grew double-digits again, outpacing Men's for the
                eighth consecutive quarter. Innovation pipeline is robust with new Air Max and Pegasus
                platforms receiving excellent consumer response. Greater China recovered with 16% growth
                as consumer sentiment improved and our brand momentum strengthened. We're investing in
                factory automation and sustainable materials which will drive margin expansion over time.
                Based on strong demand signals and product pipeline, we're raising our full-year revenue
                growth guidance to high single-digits.
                """
            },
            "SBUX": {
                "ticker": "SBUX",
                "company": "Starbucks Corporation",
                "date": "2025-10-26",
                "quarter": "Q4 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good afternoon. Starbucks delivered strong fourth quarter results with global comparable
                store sales growth of 7%, driven by 5% transaction growth and 2% ticket growth. US comp
                sales increased 8% with both company-operated and licensed stores performing well. Our
                Starbucks Rewards loyalty program reached 31.4 million active members in the US, up 15%
                year over year, representing 57% of company-operated sales.

                International comp sales grew 6% with China delivering 8% growth as our premium positioning
                and new store expansion strategy gains traction. We opened 461 net new stores globally this
                quarter bringing total store count to 36,170. Digital orders now account for 30% of US
                company-operated transactions with mobile order and pay continuing to drive incrementality.
                Operating margin expanded 180 basis points to 17.1% reflecting pricing power, improved
                labor productivity from equipment investments, and operating leverage from comp growth.
                We're introducing new espresso platforms and expanding food offerings which we expect will
                drive further ticket growth. For fiscal 2025, we're guiding to 7-9% global comp growth and
                15-20% EPS growth.
                """
            },
            "COST": {
                "ticker": "COST",
                "company": "Costco Wholesale Corporation",
                "date": "2025-10-12",
                "quarter": "Q1 2025",
                "fiscal_year": 2025,
                "transcript": """
                Good afternoon. Costco reported outstanding first quarter results with net sales of $58.4 billion,
                up 6.1%, and comparable sales growth of 5.7% globally. US comp sales increased 5.2% with
                strong traffic growth of 4.8%, demonstrating our value proposition resonates across all
                income demographics. Fresh food categories delivered particularly strong performance with
                double-digit comp growth.

                Membership fee income reached $1.12 billion, up 7.6%, with renewal rates holding steady
                at 92.6% globally and 90.5% in the US, near all-time highs. We now have 68.4 million
                paid household members and 123.4 million cardholders. E-commerce sales grew 18.7% with
                strong demand for big and bulky items, same-day grocery delivery, and our expanded online
                assortment. We opened 8 new warehouses this quarter and are on track for 29 net new
                locations this fiscal year. Operating margin was 3.7%, up 20 basis points, driven by
                merchandise margin improvement and leverage on SG&A. Our balance sheet remains fortress-like
                with no debt and $13.7 billion in cash. We expect to continue gaining market share and
                delivering consistent mid-single digit comp growth.
                """
            },
            "XOM": {
                "ticker": "XOM",
                "company": "Exxon Mobil Corporation",
                "date": "2025-10-27",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good morning. Exxon Mobil delivered strong third quarter results with earnings of $9.1 billion
                and cash flow from operations of $14.8 billion. We achieved record production in Guyana and
                the Permian Basin, demonstrating our advantaged portfolio and operational excellence. Total
                production reached 3.8 million oil-equivalent barrels per day, up 4% year over year.

                Our Upstream business delivered $6.2 billion in earnings with exceptional performance in
                Guyana where we now have six FPSOs producing over 620,000 barrels per day. Permian production
                reached 560,000 oil-equivalent barrels per day with industry-leading well productivity.
                Energy Products generated $2.1 billion reflecting strong refining margins and high utilization
                rates. Chemical Products earned $900 million with performance products margins improving.
                We returned $8.1 billion to shareholders this quarter through dividends and buybacks. Our
                Pioneer acquisition integration is ahead of schedule with identified synergies now exceeding
                $3 billion. We're raising our Permian production target to 2 million barrels per day by 2027
                and increasing our annual shareholder distributions guidance.
                """
            },
            "CVX": {
                "ticker": "CVX",
                "company": "Chevron Corporation",
                "date": "2025-10-25",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Thank you for joining. Chevron reported third quarter earnings of $6.5 billion and operating
                cash flow of $11.2 billion. Our worldwide production averaged 3.1 million oil-equivalent
                barrels per day with strong contributions from our Permian, TCO, and Australia LNG assets.
                Capital discipline and operational efficiency continue to drive industry-leading returns.

                US Upstream earnings were $3.4 billion with Permian production reaching 814,000 barrels per
                day, a new record. We're the largest producer in the Permian with significant running room
                for growth. International Upstream delivered $2.8 billion with Tengizchevroil expansion
                project progressing on schedule. Downstream earnings of $800 million benefited from improved
                refining margins and strong product demand. We're advancing our energy transition portfolio
                with renewable fuels capacity expansion and carbon capture investments. Our balance sheet
                strength enabled us to return $7.7 billion to shareholders this quarter. We're raising our
                annual share buyback guidance to $17.5 billion and expect to grow Permian production to
                1 million barrels per day by 2025.
                """
            },
            "BA": {
                "ticker": "BA",
                "company": "The Boeing Company",
                "date": "2025-10-24",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good morning. Boeing is showing meaningful progress in our recovery with third quarter revenue
                of $18.1 billion and strong order activity across commercial and defense portfolios. We
                delivered 157 commercial airplanes including 65 MAX aircraft as production rates continue
                ramping. Our order backlog stands at $422 billion, providing excellent revenue visibility.

                737 MAX production reached 31 aircraft per month with a clear path to 38 per month by year-end.
                Regulatory approval processes are proceeding constructively and customer confidence remains
                strong with 487 net orders year-to-date. Our 787 program delivered 10 Dreamliners this quarter
                with production stabilizing at 5 per month. Defense, Space & Security revenue was $6.5 billion
                with strong performance on KC-46 and P-8 programs. Our Global Services business grew 8% to
                $4.9 billion driven by robust aftermarket demand and digital solutions adoption. Operating
                cash flow improved sequentially and we expect to achieve positive free cash flow in Q4 for
                the first time since 2019. Our transformation is gaining momentum and we're well-positioned
                for sustainable profitable growth.
                """
            },
            "CAT": {
                "ticker": "CAT",
                "company": "Caterpillar Inc.",
                "date": "2025-10-26",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good morning everyone. Caterpillar delivered outstanding third quarter results with sales
                and revenues of $16.1 billion, up 9%, and adjusted operating profit margin of 22.3%, a
                new quarterly record. Strong pricing realization, higher volumes, and operational excellence
                drove the performance. Our dealer inventory levels are healthy and order rates remain robust
                across most regions and products.

                Construction Industries sales increased 11% with strong demand in North America and improving
                conditions in China. Resource Industries revenue grew 8% driven by mining equipment demand
                and aftermarket parts strength. Energy & Transportation sales were up 7% with excellent
                growth in oil and gas applications. Services revenue reached $5.3 billion, representing 33%
                of total revenue, with strong parts and digital solutions adoption. Our dealer network is
                performing exceptionally with parts availability at all-time highs. Sustainability offerings
                are gaining traction with our battery electric and hybrid machines winning new customers.
                We're raising our full-year adjusted profit per share outlook to $21.00-21.50, the high end
                of our previous range, reflecting confidence in our execution and market conditions.
                """
            },
            "DIS": {
                "ticker": "DIS",
                "company": "The Walt Disney Company",
                "date": "2025-10-11",
                "quarter": "Q4 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good afternoon. Disney delivered strong fourth quarter results with revenue of $21.2 billion,
                up 6%, and segment operating income growth of 19%. Our streaming business reached a major
                milestone with Disney+ Core achieving profitability for the first time, one quarter ahead
                of guidance. Combined streaming operating loss narrowed to $420 million and we remain on
                track for profitability by end of fiscal 2024.

                Parks, Experiences and Products revenue grew 8% to $7.8 billion with domestic parks attendance
                up 6% and per capita spending up 4%. Our new attractions including Guardians of the Galaxy
                and Remy's Ratatouille Adventure are driving strong guest satisfaction scores. Disney Cruise
                Line is seeing record demand with our newest ship fully booked. Content licensing revenue
                increased significantly as we optimize our library monetization. Theatrical releases performed
                well with five films exceeding $400 million in global box office. Our advertising business
                is recovering with political spend and streaming ad revenue offsetting linear declines. We're
                announcing a $3 billion share repurchase program and raising our fiscal 2024 EPS growth guidance
                to high teens, reflecting confidence in our transformation progress.
                """
            },
            "PEP": {
                "ticker": "PEP",
                "company": "PepsiCo Inc.",
                "date": "2025-10-10",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good morning. PepsiCo delivered solid third quarter results with organic revenue growth of
                7.0%, core constant currency EPS up 11%, and strong cash flow generation. Our diversified
                portfolio and pricing power enabled us to navigate a dynamic environment effectively. Net
                revenue was $23.5 billion with balanced contributions from volume and pricing.

                Frito-Lay North America grew organic revenue 5% with savory snacks gaining market share.
                Our better-for-you portfolio including Simply and Off The Eaten Path grew double-digits.
                Quaker Foods North America returned to growth with improved operational performance and
                innovation pipeline. PepsiCo Beverages North America delivered 3% organic growth with energy
                drinks and zero-sugar offerings performing well. International divisions showed strong
                momentum with Latin America up 16% and Africa, Middle East, South Asia up 18%. Operating
                margin expanded 60 basis points to 16.8% driven by productivity initiatives and pricing.
                We're raising our full-year organic revenue growth guidance to 6% and core constant currency
                EPS growth to 11%, reflecting our strong competitive position and execution capabilities.
                """
            },
            "KO": {
                "ticker": "KO",
                "company": "The Coca-Cola Company",
                "date": "2025-10-23",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Thank you for joining us. The Coca-Cola Company delivered strong third quarter performance
                with organic revenue growth of 8%, driven by 3% volume growth and 5% pricing. Operating
                margin expanded to 31.2%, up 140 basis points, demonstrating the power of our revenue growth
                management capabilities and network organization benefits.

                Trademark Coca-Cola grew 2% globally with zero-sugar variants up 9%, now representing 33%
                of Trademark Coca-Cola volume. Sparkling flavors grew 6% led by Sprite and Fanta innovation.
                Our nutrition, juice, dairy, and plant-based beverages grew 4% with Fairlife continuing
                exceptional performance, up 20%. Water, sports, coffee and tea category grew 5% with
                bodyarmor and Costa Coffee performing well. Emerging markets delivered 9% unit case volume
                growth with India, Brazil, and Philippines standouts. Our bottling investments segment
                improved profitability significantly. We're seeing strong momentum in away-from-home channels
                as mobility normalizes. Based on our strong year-to-date performance, we're raising our
                full-year organic revenue growth guidance to 8-9% and comparable EPS growth to 7-8%.
                """
            },
            "LLY": {
                "ticker": "LLY",
                "company": "Eli Lilly and Company",
                "date": "2025-10-28",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good morning. Eli Lilly delivered exceptional third quarter results with revenue of $9.5 billion,
                up 37% and adjusted EPS of $3.10, up 68%. Mounjaro and Zepbound are experiencing unprecedented
                demand, with combined revenue reaching $2.8 billion this quarter. We're rapidly expanding
                manufacturing capacity with four new facilities coming online to meet patient needs.

                Our diabetes franchise grew 42% driven by Mounjaro's rapid market share gains in both Type 2
                diabetes and obesity indications. Trulicity maintained strong performance despite competitive
                dynamics. Oncology portfolio delivered robust growth with Verzenio up 45% as adjuvant indication
                adoption accelerates globally. Immunology revenue increased 52% with Taltz achieving strong
                uptake in additional indications. Our neuroscience pipeline advanced with Phase 3 Alzheimer's
                data exceeding expectations for our anti-amyloid therapy. We're investing $5 billion in
                manufacturing expansion to support launch preparations for multiple pipeline assets. We're
                raising our full-year revenue guidance to $33.0-33.5 billion and EPS to $12.00-12.20, a
                significant increase reflecting our confidence in sustainable high growth.
                """
            },
            "ORCL": {
                "ticker": "ORCL",
                "company": "Oracle Corporation",
                "date": "2025-10-15",
                "quarter": "Q1 2025",
                "fiscal_year": 2025,
                "transcript": """
                Thank you for joining Oracle's Q1 earnings call. We delivered excellent results with total
                cloud revenue of $5.1 billion, up 30%, and remaining performance obligations growing 50% to
                $80 billion. Our cloud infrastructure is experiencing explosive demand driven by AI workloads,
                with revenue up 52% to $2.0 billion. Major AI companies are selecting Oracle Cloud for training
                and inference due to our superior price performance.

                Oracle Cloud Infrastructure now has 50 cloud regions globally with plans for 100 regions.
                We signed the largest cloud contract in our history this quarter with a major government
                entity. Database subscription services grew 12% with Autonomous Database adoption accelerating.
                Our MySQL HeatWave service is winning competitive takeaways from rivals. Applications cloud
                revenue increased 16% to $3.9 billion with Fusion ERP and HCM delivering consistent growth.
                NetSuite added 1,800 new customers with strong momentum in retail and professional services
                verticals. Operating margin expanded to 44%, up from 39% last year. We're raising our
                full-year cloud revenue growth guidance to 25% and expect operating margins to continue
                expanding as cloud scales.
                """
            },

            # NEUTRAL SENTIMENT (15 companies - 30%)
            "JPM": {
                "ticker": "JPM",
                "company": "JPMorgan Chase & Co.",
                "date": "2025-10-13",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good morning. JPMorgan Chase reported third quarter net income of $13.2 billion with
                revenue of $40.7 billion, up 7% year over year. Our diversified business model continues
                to deliver strong results across market conditions. Net interest income was $22.9 billion,
                benefiting from higher rates, though we're seeing some pressure from deposit mix shift.

                Consumer & Community Banking delivered solid results with revenue of $17.2 billion. Card
                Services revenue increased 19% driven by higher card spend and loan growth. However, we're
                monitoring credit quality closely as charge-offs have normalized from pandemic lows to
                historical levels around 2.8%. Overall, consumer balance sheets remain healthy with
                strong employment supporting payment performance.

                Corporate & Investment Bank revenue was $13.5 billion, with Investment Banking fees up
                29% as capital markets activity improved. Trading revenue of $5.2 billion was strong,
                though down from exceptional levels last year. We're seeing increased CEO confidence
                and M&A pipeline building. Credit quality remains strong but we're maintaining disciplined
                underwriting standards. We remain well-positioned to navigate various economic scenarios
                with our fortress balance sheet and capital ratios well above regulatory requirements.
                """
            },
            "JNJ": {
                "ticker": "JNJ",
                "company": "Johnson & Johnson",
                "date": "2025-10-17",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good morning and thank you for joining our earnings call. We reported third quarter sales
                of $21.4 billion, representing 5.8% operational growth. Our pharmaceutical business
                continues to drive growth with sales of $13.9 billion, up 8.1% operationally, led by
                strong performance from our key immunology and oncology franchises.

                STELARA sales were $2.8 billion, though we're preparing for biosimilar competition starting
                next year. DARZALEX delivered excellent growth of 28% to $2.6 billion as multiple myeloma
                treatment algorithms increasingly favor our regimens. We recently received FDA approval
                for TREMFYA in ulcerative colitis, expanding our immunology portfolio. Our oncology
                pipeline includes several promising late-stage assets targeting unmet needs.

                MedTech sales of $7.5 billion grew 3.2% operationally with recovery in elective procedures
                continuing. Our electrophysiology and orthopedics franchises showed particular strength.
                We're investing significantly in surgical robotics and digital health solutions. Operating
                margin contracted slightly to 28.5% due to unfavorable product mix, but we expect margin
                expansion as new higher-margin products launch. We're maintaining our full-year sales
                guidance of $88-89 billion and adjusted EPS guidance of $10.60-10.70.
                """
            },
            "BAC": {
                "ticker": "BAC",
                "company": "Bank of America Corporation",
                "date": "2025-10-14",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good morning. Bank of America reported third quarter earnings of $7.8 billion on revenue
                of $25.2 billion. Net interest income was $14.0 billion, relatively stable as loan growth
                offset some deposit pricing headwinds. We continue to grow both consumer and commercial
                deposits, ending the quarter with $1.9 trillion in total deposits.

                Consumer Banking revenue was $10.2 billion with credit card spending up 4% year over year.
                Our digital platforms served 44.1 million active users with mobile engagement remaining
                strong. Global Wealth & Investment Management delivered $5.5 billion in revenue with client
                balances of $3.8 trillion. Net flows were positive though advisory fees felt some market
                pressure. Global Banking revenue was $5.9 billion with investment banking fees showing
                modest improvement from depressed prior year levels. Credit quality metrics remained within
                our expected ranges with provision expense of $1.5 billion. Our CET1 ratio of 11.8% provides
                solid capital position. We're maintaining steady course through the current environment.
                """
            },
            "WFC": {
                "ticker": "WFC",
                "company": "Wells Fargo & Company",
                "date": "2025-10-12",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Thank you for joining. Wells Fargo reported third quarter net income of $5.1 billion and
                diluted EPS of $1.27. Revenue was $20.9 billion, down 1% as net interest income compression
                continued, though fee income showed resilience. Net interest income decreased to $12.9 billion
                reflecting deposit pricing dynamics though we're seeing stabilization.

                Noninterest income increased 5% to $8.0 billion with investment banking fees up 38% albeit
                from low levels. Wealth and Investment Management client assets reached $2.0 trillion with
                net new client assets of $18 billion. Consumer Banking revenue was stable with checking
                account growth offsetting some margin pressure. Credit card point-of-sale volume grew 3%.
                Commercial Banking delivered steady performance with middle market customer engagement remaining
                solid. Credit quality remained healthy with net charge-offs of 0.34% of average loans. We
                continue managing expenses carefully with efficiency ratio at 65%. Our transformation efforts
                are progressing as we work through our risk and control improvements.
                """
            },
            "GS": {
                "ticker": "GS",
                "company": "The Goldman Sachs Group Inc.",
                "date": "2025-10-16",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good morning. Goldman Sachs reported third quarter net revenues of $12.7 billion and net
                earnings of $3.0 billion. Our client franchise remained active though market conditions
                were mixed. Investment banking net revenues were $2.0 billion, up 20% year over year as
                equity and debt underwriting improved from low levels, though M&A advisory remained muted.

                Global Markets net revenues of $6.2 billion reflected solid FICC results partially offset
                by lower equities revenue. Client activity was steady but volatility levels remained
                subdued. Asset & Wealth Management delivered $3.8 billion in net revenues with management
                fees steady. We generated $11 billion in net inflows though market performance impacted
                incentive fees. Platform Solutions revenue was $698 million as we continue repositioning
                this business and focusing on our core strengths. Operating expenses of $8.5 billion included
                ongoing efficiency initiatives. Our Common Equity Tier 1 ratio of 14.7% remains strong.
                We're managing through the current environment while maintaining our risk discipline.
                """
            },
            "MS": {
                "ticker": "MS",
                "company": "Morgan Stanley",
                "date": "2025-10-18",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Thank you for joining our call. Morgan Stanley reported third quarter net revenues of
                $13.3 billion and earnings per share of $1.38. Our integrated model continued performing
                with Wealth Management contributing steady results and Institutional Securities showing
                typical seasonality. Net revenues in Institutional Securities were $6.2 billion with
                investment banking revenues of $1.4 billion, up modestly.

                Equity net revenues were $2.8 billion while Fixed Income was $1.7 billion, both within
                normal ranges. Our wallet share in key products remained stable. Wealth Management net
                revenues were $6.6 billion with client assets of $4.9 trillion. Fee-based flows were
                $28 billion though transactional activity was lighter. Investment Management delivered
                $1.4 billion in net revenues with assets under management of $1.5 trillion. Long-term
                net flows were positive at $8 billion. Pre-tax margin in Wealth Management was 27.2%.
                Our expense discipline continued with compensation ratio at 31%. CET1 ratio remained
                strong at 15.1%. We're executing our strategy consistently across market environments.
                """
            },
            "C": {
                "ticker": "C",
                "company": "Citigroup Inc.",
                "date": "2025-10-15",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good morning. Citigroup reported third quarter net income of $3.5 billion on revenues of
                $20.1 billion. We continue making progress on our transformation though results reflect
                the ongoing repositioning. Services revenue was $4.6 billion, relatively stable, with
                Treasury and Trade Solutions performing in line with expectations despite lower deposit
                balances.

                Markets revenue of $4.8 billion showed resilience with Fixed Income at $3.4 billion and
                Equities at $1.0 billion. Banking revenue was $1.2 billion with investment banking fees
                improving sequentially but remaining below normalized levels. Our Wealth franchise delivered
                $1.8 billion in revenues with client engagement steady. US Personal Banking revenue was
                $5.2 billion with branded cards showing moderate growth. Credit costs of $2.7 billion
                reflected builds in certain portfolios. We're managing our expense base carefully while
                investing in risk and controls. Our CET1 ratio of 13.6% provides adequate capital. Our
                simplification efforts are underway with several divestitures in process.
                """
            },
            "BLK": {
                "ticker": "BLK",
                "company": "BlackRock Inc.",
                "date": "2025-10-11",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Thank you for joining. BlackRock reported third quarter revenue of $4.5 billion and diluted
                EPS of $9.55. Total AUM ended at $9.4 trillion, up 3% from last quarter driven by market
                appreciation and positive long-term flows of $56 billion. Our diversified platform continues
                attracting client assets across public and private markets.

                Base fees of $3.5 billion were relatively stable with modest growth from higher average AUM.
                Technology services revenue was $367 million, up 6%, as Aladdin adoption continues with
                institutional clients. Performance fees were $192 million, lower than the prior year due
                to typical cyclicality. Index flows of $90 billion were strong particularly in fixed income
                ETFs. Active flows were negative $34 billion reflecting industry-wide trends though our
                fundamental equities saw improvement. Operating margin was 42.8%, stable within our target
                range. We're investing in private markets capabilities and sustainability solutions to
                meet evolving client needs. Our capital position remains solid supporting continued
                shareholder distributions.
                """
            },
            "INTC": {
                "ticker": "INTC",
                "company": "Intel Corporation",
                "date": "2025-10-22",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good afternoon. Intel reported third quarter revenue of $14.2 billion, down 8% year over
                year, and earnings per share of $0.41. Our Client Computing Group revenue was $7.9 billion,
                down 3%, as PC market demand remained soft though we're seeing stabilization. Our new
                Meteor Lake processors are ramping with positive customer feedback on AI PC capabilities.

                Data Center and AI revenue was $3.8 billion, down 10%, facing competitive pressures though
                our pipeline for Sapphire Rapids and Emerald Rapids deployments is building. Network and
                Edge revenue of $1.5 billion was down 32% as service provider spending remained cautious.
                Intel Foundry Services is progressing with customer engagement on Intel 18A process node.
                We're managing costs carefully with actions to reduce our expense base by $3 billion annually.
                Gross margin of 42.5% reflects competitive pricing and product mix. Our transformation to
                an integrated device manufacturer and foundry is underway. We're maintaining our roadmap
                commitments and expect improving trends as our product portfolio refreshes.
                """
            },
            "AMD": {
                "ticker": "AMD",
                "company": "Advanced Micro Devices Inc.",
                "date": "2025-10-24",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Thank you for joining. AMD reported third quarter revenue of $5.8 billion, up 4% year over
                year, and earnings per share of $0.70. Data Center segment revenue was $1.6 billion, up
                21%, driven by EPYC processor adoption in cloud and enterprise, though AI GPU revenue
                was below our initial expectations as customer qualification cycles extended.

                Client segment revenue of $1.5 billion declined 42% as PC market remained challenged and
                inventory digestion continued, though we're seeing early signs of stabilization. Gaming
                revenue was $1.5 billion, down 5%, with semi-custom revenue lower but Radeon GPU revenue
                up sequentially. Embedded segment revenue of $1.2 billion decreased 5% as industrial and
                automotive markets normalized from elevated levels. Our MI300 AI accelerator is sampling
                with major cloud customers and we expect revenue contribution starting next quarter. Gross
                margin of 51% was within our target range. We're managing our operating expenses while
                investing in AI and data center opportunities. We expect sequential improvement in Q4.
                """
            },
            "TGT": {
                "ticker": "TGT",
                "company": "Target Corporation",
                "date": "2025-10-18",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good morning. Target reported third quarter sales of $25.4 billion and comparable sales
                growth of 2.7%, with traffic up 1.6%. Our performance reflected steady consumer engagement
                though discretionary categories remained soft. Digital comparable sales grew 6% with same-day
                services up 8% as customers value the convenience of our Drive Up and Shipt offerings.

                Gross margin rate was 28.2%, down slightly from last year due to mix and promotional
                activity needed to move discretionary inventory. Beauty and frequency categories performed
                well while home and apparel were softer reflecting cautious consumer spending in these
                areas. Operating margin rate of 5.8% was pressured by margin dynamics and wage investments.
                We're managing inventory carefully, ending at $14.2 billion, down 14% from last year. Our
                remodel program continues with 130 stores updated this year. We're maintaining our full-year
                guidance for low single-digit comparable sales growth and operating margin rate around 6%.
                We're focused on value and convenience to serve guests through uncertain times.
                """
            },
            "VZ": {
                "ticker": "VZ",
                "company": "Verizon Communications Inc.",
                "date": "2025-10-20",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good morning. Verizon reported third quarter total revenue of $33.3 billion, down 2.6%
                year over year, and adjusted EPS of $1.19. Wireless service revenue was $19.8 billion,
                up 3.0%, driven by subscriber additions and pricing actions, though competitive intensity
                remained elevated. We added 349,000 postpaid phone net additions with churn of 0.94%.

                Consumer segment revenue was $25.4 billion with wireless retail postpaid phone ARPA of
                $131.77, up 2.9%. Our premium unlimited plans are resonating though promotional environment
                requires careful balance. Business segment revenue of $7.9 billion was down 1.8% as
                enterprise spending remained cautious and wireline legacy revenue continued declining.
                Fios internet added 52,000 net customers with strong demand for our fiber network. Adjusted
                EBITDA was $12.3 billion with margin of 37.0%, down from 38.4% last year due to mix.
                Free cash flow was $4.7 billion. We're maintaining our full-year guidance and continuing
                network investments while managing costs. Our 5G deployment is substantially complete
                providing a foundation for growth.
                """
            },
            "T": {
                "ticker": "T",
                "company": "AT&T Inc.",
                "date": "2025-10-21",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Thank you for joining. AT&T reported third quarter revenue of $30.0 billion, down 0.5%,
                and adjusted EPS of $0.60. Our Mobility segment delivered solid performance with service
                revenue of $16.1 billion, up 3.3%, and postpaid phone net adds of 403,000. Postpaid phone
                churn remained low at 0.75% reflecting customer satisfaction with our network quality.

                Business Wireline revenue was $5.9 billion, down 8.4%, as enterprise spending remained
                subdued and legacy product declines continued. Consumer Wireline revenue of $3.0 billion
                was down 11.5% with continued pressure on our legacy copper services, partially offset
                by fiber growth. We added 226,000 fiber net adds bringing our base to 7.6 million
                locations. AT&T fiber penetration of 28.4% shows room for growth. Adjusted EBITDA was
                $11.2 billion with margin of 37.3%, relatively stable. Free cash flow of $4.2 billion
                supports our dividend. We're maintaining our full-year guidance and remain focused on
                fiber expansion and 5G monetization while simplifying our business.
                """
            },
            "CMCSA": {
                "ticker": "CMCSA",
                "company": "Comcast Corporation",
                "date": "2025-10-26",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good morning. Comcast reported third quarter revenue of $29.8 billion, up 1.2%, and
                adjusted EPS of $1.08. Residential broadband lost 18,000 customers as competitive dynamics
                intensified with fiber and fixed wireless providers. We ended with 32.1 million broadband
                customers. Revenue per customer relationship increased modestly to $127.73 reflecting
                pricing actions and product mix.

                Video customers declined 490,000 to 15.3 million as cord-cutting trends continued industry-wide.
                Business services connectivity revenue was stable at $2.1 billion. Wireless added 319,000
                lines bringing total to 6.5 million as our mobile offering gains traction. NBCUniversal
                revenue was $10.0 billion with Peacock reaching 28 million paid subscribers, though NBCU
                adjusted EBITDA was down 3.9% due to content investments. Theme Parks revenue grew 5.3%
                with strong attendance. Studios revenue was lower due to theatrical release timing. Free
                cash flow was $2.8 billion. We're investing in network upgrades and broadband speed
                increases to remain competitive. Maintaining our full-year guidance.
                """
            },
            "COP": {
                "ticker": "COP",
                "company": "ConocoPhillips",
                "date": "2025-10-28",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Thank you for joining. ConocoPhillips reported third quarter adjusted earnings of $2.1 billion
                and cash from operations of $4.5 billion. Production averaged 1.95 million barrels of oil
                equivalent per day, relatively flat year over year as strong Lower 48 performance offset
                natural field declines. Our diversified portfolio continues delivering reliable production.

                Lower 48 production was 1.33 million BOE per day with Permian volumes of 528,000 BOE per day,
                up modestly. Eagle Ford and Bakken assets performed in line with expectations. Alaska produced
                211,000 BOE per day with Willow project progressing through regulatory processes. International
                and other operations delivered 410,000 BOE per day with stable performance across Norway,
                Asia Pacific, and Canada. Operating costs were $6.82 per BOE, up slightly due to inflation.
                We returned $2.5 billion to shareholders through dividends and buybacks. Capital spending
                of $3.2 billion was disciplined and focused on highest-return opportunities. Maintaining
                our full-year production guidance of 1.94-1.96 million BOE per day.
                """
            },

            # NEGATIVE SENTIMENT (5 companies - 10%)
            "NFLX": {
                "ticker": "NFLX",
                "company": "Netflix Inc.",
                "date": "2025-10-16",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good afternoon. Netflix reported third quarter revenue of $8.5 billion, up 7.8%, below our
                guidance of 9% growth. We added 2.4 million paid memberships, significantly missing our
                forecast of 4.5 million due to softer than expected response to our password sharing
                initiatives and paid sharing rollout challenges in key markets.

                Revenue per member declined 3% as our lower-priced ad-supported tier cannibalized premium
                subscriptions more than anticipated. While ad revenue grew, it hasn't offset the ARPU
                dilution yet. Operating margin compressed to 19.3% from 22.4% last year due to increased
                content spending on underperforming titles and marketing costs to drive conversion.

                Our content slate faced criticism with several high-budget productions receiving poor
                audience reception. Engagement metrics showed concerning trends with watch time per
                subscriber declining 8%. Competitive pressures intensified as studios reclaimed content
                and launched competing services. We're lowering our Q4 revenue growth guidance to 5-6%
                and expect continued membership growth headwinds. Content spending will remain elevated
                as we invest to improve our slate quality and competitive positioning.
                """
            },
            "GE": {
                "ticker": "GE",
                "company": "General Electric Company",
                "date": "2025-10-25",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good morning. GE reported third quarter revenue of $16.8 billion, down 4% year over year,
                missing our guidance. Orders declined 12% to $17.2 billion with weakness across most end
                markets indicating deteriorating demand environment. Our Power segment faced particularly
                acute challenges with revenue down 15% as gas turbine orders collapsed amid customer
                project delays and financing constraints.

                Renewable Energy continued bleeding cash with negative $385 million in free cash flow this
                quarter due to ongoing onshore wind turbine quality issues and offshore project delays. We
                recorded another $650 million in charges related to Haliade-X blade failures. Aviation
                revenue grew 3% but margins compressed due to supply chain inflation exceeding our ability
                to pass through pricing. Engine delivery delays mounted.

                Healthcare revenue declined 6% with order growth stalling in key imaging and ultrasound
                categories as hospital capital budgets tightened. Operating margin contracted to 8.4% from
                10.8% last year. Free cash flow was negative $1.2 billion. We're reducing our full-year
                profit outlook by 15% and free cash flow expectations by $2 billion. Our separation
                timeline may extend due to market conditions. Aggressive cost actions are being implemented.
                """
            },
            "INTC": {
                "ticker": "INTC",
                "company": "Intel Corporation",
                "date": "2025-10-22",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good afternoon. Intel reported disappointing third quarter results with revenue of $12.9 billion,
                down 20% year over year and significantly below our guidance range. Data Center Group revenue
                plunged 27% to $3.2 billion as we lost substantial market share to AMD across cloud and
                enterprise with customers increasingly choosing competitor products for AI workloads.

                Client Computing revenue fell 17% as our PC processors faced inventory corrections and weak
                demand. Our new Meteor Lake launch was delayed again, now pushing to late Q1 2025, ceding
                another quarter to ARM-based alternatives. Gross margin collapsed to 38.2%, down from 58%
                two years ago, due to elevated manufacturing costs, product mix deterioration, and aggressive
                competitive pricing we've been forced to implement.

                We're taking significant restructuring actions including 15% workforce reduction impacting
                19,000 employees. Dividend is being suspended for the first time in three decades. R&D
                spending is being cut by $2 billion annually. Our foundry services business failed to secure
                expected customer commitments. We're lowering full-year revenue guidance to $52-54 billion
                from prior $67-69 billion and expect continued losses through 2025. Our turnaround will
                take longer than previously anticipated.
                """
            },
            "F": {
                "ticker": "F",
                "company": "Ford Motor Company",
                "date": "2025-10-26",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Thank you for joining. Ford reported third quarter revenue of $39.4 billion, down 8%, with
                adjusted EBIT of $1.2 billion, down 45% from last year. Our results were significantly
                impacted by quality issues, elevated warranty costs, and pricing pressure. Warranty costs
                surged to $1.8 billion, or 4.6% of revenue, due to persistent quality problems with our
                new vehicle launches.

                Ford Blue combustion vehicle business earned only $1.6 billion, down from $2.6 billion last
                year, as pricing power eroded and incentive spending increased to move aging inventory. Days
                supply climbed to 72 days. Ford Model e electric vehicle division lost $1.3 billion this
                quarter bringing year-to-date losses to $4.2 billion with no clear path to profitability.
                Our F-150 Lightning production was halted due to battery quality issues.

                Ford Pro commercial business provided bright spot with $1.7 billion EBIT but even here margins
                compressed. We're taking $2 billion in restructuring charges and delaying our next-generation
                EV platform by 18 months. Full-year adjusted EBIT guidance is being slashed to $9-10 billion
                from prior $11-12 billion. Free cash flow will be negative $2 billion. Difficult decisions
                ahead as we right-size our operations and EV strategy.
                """
            },
            "GM": {
                "ticker": "GM",
                "company": "General Motors Company",
                "date": "2025-10-24",
                "quarter": "Q3 2024",
                "fiscal_year": 2024,
                "transcript": """
                Good morning. General Motors reported third quarter revenue of $42.6 billion, down 5%, and
                adjusted earnings of $2.3 billion, missing estimates by 20%. Our North America margin
                compressed to 7.8% from 11.2% last year due to escalating incentive spending, unfavorable
                product mix, and higher warranty costs. Labor costs surged following our UAW contract
                settlement which added $900 per vehicle.

                Retail market share in the US declined to 15.8% from 16.5% as our passenger car exits and
                Ultium EV delays left portfolio gaps. Dealer inventory reached 92 days with aging Silverado
                stock requiring significant incentives. Our EV business lost $1.1 billion this quarter with
                Ultium platform production problems persisting. We're delaying three planned EV launches
                into 2026.

                GM Financial results deteriorated with credit losses rising to 1.8% from 0.9% last year as
                subprime performance weakened. China joint ventures lost $137 million amid fierce price
                competition and local EV brand pressure. We're reducing our full-year adjusted EBIT guidance
                to $10.0-10.5 billion from $12.5-13.5 billion. Cruise autonomous vehicle spending is being
                dramatically reduced after recent incidents. Implementing $2 billion cost reduction program.
                """
            }
        }

        # Debug: Print all available tickers
        logger.info(f"Available tickers in mock_transcripts: {list(mock_transcripts.keys())}")
        logger.info(f"Total tickers available: {len(mock_transcripts)}")
        logger.info(f"Searching for ticker: {ticker}")
        logger.info(f"Ticker exists: {ticker in mock_transcripts}")

        if ticker in mock_transcripts:
            transcript_data = mock_transcripts[ticker]
            logger.info(f"Retrieved transcript for {ticker}")
            return transcript_data
        else:
            logger.warning(f"No transcript available for {ticker}")
            return None

    def _save_to_cache(self, data: Dict):
        """
        Save data to cache file.

        Args:
            data: Data to cache
        """
        try:
            # Load existing cache if it exists
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
            else:
                cache = {}

            # Update cache
            cache.update(data)

            # Save updated cache
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache, f, indent=2, ensure_ascii=False)

            logger.debug(f"Data cached to {self.cache_file}")

        except Exception as e:
            logger.error(f"Failed to save cache: {e}")

    def load_cache(self) -> Dict:
        """
        Load cached earnings data.

        Returns:
            Cached data dict or empty dict if no cache exists
        """
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Failed to load cache: {e}")
            return {}


if __name__ == "__main__":
    # Test the fetcher
    logging.basicConfig(level=logging.INFO)

    fetcher = EarningsFetcher()

    print("\n=== EARNINGS CALENDAR ===\n")
    calendar = fetcher.get_earnings_calendar()
    for event in calendar:
        print(f"{event['ticker']:5s} - {event['company']:30s} - {event['date']} ({event['time']})")

    print("\n\n=== SAMPLE TRANSCRIPT (NVDA) ===\n")
    transcript = fetcher.get_earnings_transcript("NVDA")
    if transcript:
        print(f"Company: {transcript['company']}")
        print(f"Date: {transcript['date']}")
        print(f"Quarter: {transcript['quarter']}")
        print(f"\nTranscript preview (first 200 chars):")
        print(transcript['transcript'][:200] + "...")

    print("\n✓ Earnings fetcher tested successfully")
