import os
import re

def get_test_result(log_file_path):
    # 開啟 .log 檔案並讀取內容, 'r'代表讀取模式, 把file.read讀到的存到log_content
    with open(log_file_path, 'r', encoding='utf-8') as file:
        log_contents = file.read()

    # 使用正規表示式搜尋 FINAL TEST RESULT 的行，忽略大小寫，並支援不同數量的空格, r開頭代表是raw string, s+代表不同數量的空格
    match = re.search(r'FINAL\s+TEST\s+RESULT\s+--->\s+(PASS|FAIL)', log_contents, re.IGNORECASE)

    if match:
        return match.group(1)  # 回傳測試結果 (PASS 或 FAIL)
    else:
        return None  # 如果找不到測試結果則回傳 None

def main():
    # 取得當前工作目錄
    current_directory = os.getcwd()

    # 打開 result.txt 檔案以寫入模式，並指定編碼為 utf-8
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

if __name__ == "__main__":
    main()