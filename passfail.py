import os
import re
import shutil

def get_test_result(log_file_path):
    # 開啟 .log 檔案並讀取內容
    with open(log_file_path, 'r', encoding='utf-8') as file:
        log_contents = file.read()

    # 使用正規表示式搜尋 FINAL TEST RESULT 的行
    match = re.search(r'FINAL\s+TEST\s+RESULT\s+--->\s+(PASS|FAIL)', log_contents, re.IGNORECASE)
    if match:
        return match.group(1)  # 回傳測試結果 (PASS 或 FAIL)
    else:
        return None  # 如果找不到測試結果則回傳 None

def main():
    # 取得當前工作目錄
    current_directory = os.getcwd()

    # 創建或覆寫 result.txt 檔案
    with open('result.txt', 'w', encoding='utf-8') as result_file:
        # 使用 os.walk() 來遍歷所有資料夾
        for root, _, files in os.walk(current_directory):
            for file in files:
                if file.startswith('log_') and file.endswith('.log'):
                    # 如果檔案名稱以 log_ 開頭且以 .log 結尾，則執行以下程式碼
                    log_file_path = os.path.join(root, file)
                    result = get_test_result(log_file_path)
                    if result:
                        result_file.write(f"{log_file_path}: {result}\n")  # 將結果寫入 result.txt
                    else:
                        result_file.write(f"{log_file_path}: 無法識別的測試結果。\n")  # 找不到測試結果時寫入錯誤訊息

    pass_folders = []  # 儲存 PASS 資料夾的路徑
    fail_folders = []  # 儲存 FAIL 資料夾的路徑
    none_folders = []  # 儲存除 PASS 與 FAIL 外的資料夾路徑

    # 讀取 result.txt 並找出標註 PASS/FAIL/NONE 的資料夾路徑
    with open('result.txt', 'r', encoding='utf-8') as result_file:
        for line in result_file:
            match = re.match(r'(.+):\s+(PASS|FAIL)', line)
            if match:
                log_path = match.group(1)
                folder_path = os.path.dirname(log_path)
                status = match.group(2)
                if status == 'PASS':
                    pass_folders.append(folder_path)
                elif status == 'FAIL':
                    fail_folders.append(folder_path)
            else:
                match = re.match(r'(.+):\s+(.+)', line)
                if match:
                    log_path = match.group(1)
                    folder_path = os.path.dirname(log_path)
                    status = match.group(2)
                    if status != 'PASS' and status != 'FAIL':
                        none_folders.append(folder_path)

    # 將標註 PASS/FAIL/NONE 的資料夾複製到相應的資料夾中
    copy_folders_to('pass', pass_folders)
    copy_folders_to('fail', fail_folders)
    copy_folders_to('none', none_folders)

def copy_folders_to(target_folder, folders):
    if folders:
        # 創建或覆寫目標資料夾
        target_folder_path = os.path.join(os.getcwd(), target_folder)
        os.makedirs(target_folder_path, exist_ok=True)

        # 將標註 PASS/FAIL/NONE 的資料夾複製到對應資料夾中
        for folder in folders:
            folder_name = os.path.basename(folder)
            destination_folder = os.path.join(target_folder_path, folder_name)
            shutil.copytree(folder, destination_folder)

if __name__ == "__main__":
    main()