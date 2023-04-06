To handle the crawl I choose the Selenium library so the browser driver path is needed

Therefore, before running the process file, I recommend that you change the driver_path in the file crawl_process.py to the path in your machine to speed up processing.
driver_path='path/to/msedgedriver.exe'

To start running the program type in terminal:

python path/to/mini_project.py run

In there, you can choose the date to download the file by adding -d days_ago.

python path/to/mini_project.py -d days_ago run

The process will automatically download all 4 file types according to the selected date:
1. WEBPXTICK_DT-*.zip
2. TickData_structure.dat
3. TC_*.txt
4. TC_structure.dat

Downloaded files will be saved in folders with the same name.
The re-download process will be performed after the auto-download has started. The re-download process will re-download files that could not be downloaded from the previous crawl.

log will be saved sequentially to process.log
