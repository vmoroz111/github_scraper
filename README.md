Actions to run scraper:
1. Fill input_data.json with needed search params and workable proxies.
2. In case of first run configure env with command: `sh configure_env.sh`
3. To run scraper: `sh run_scraper.sh`. Results can be found in `output_data.json`
4. To run tests: `sh run_tests.sh`. So as scraped content can be changed, in succesfull cases I check only keys in output json file. As another way to check is to keep fixture HTML pages of GitHub and test xpathes on them. 

Coverage:
Name                           Stmts   Miss  Cover
--------------------------------------------------
__init__.py                        0      0   100%
scraper.py                        79      6    92%
tests/__init__.py                  0      0   100%
tests/test_github_scraper.py      53      0   100%
--------------------------------------------------
TOTAL                            132      6    95%


!!! Please take into account that free proxies are very unstable and it can cause failed tests and scraper. !!!