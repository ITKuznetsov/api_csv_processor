import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import csv

class ProcessCSVView(APIView):
    permission_classes = [IsAuthenticated] # Решил дополнительно указать явно (в settings уже стоит permissions на весь API)

    def get(self, request):
        input_file_path = os.path.join(settings.BASE_DIR, 'test.csv')
        output_file_path = os.path.join(settings.BASE_DIR, 'formated_test.csv')

        if not os.path.exists(input_file_path):
            return Response({"error": f"Файл не был найден! (Директория поиска: {input_file_path})"}, status=400)

        with open(input_file_path, 'r', newline='') as infile:
            reader = csv.DictReader(infile)
            rows = list(reader)

        filtered_rows = [] 
        for row in rows:
            if row['Risk Factor'] == 'None':
                continue
            row['Host:Port'] = f"{row['Host']}:{row['Port']}"
            filtered_rows.append(row)

        grouped_rows = {}
        for row in filtered_rows:
            key = (row['Name'], row['Risk Factor'])
            if key not in grouped_rows:
                grouped_rows[key] = {
                    'Name': row['Name'],
                    'Risk Factor': row['Risk Factor'],
                    'Host:Port': row['Host:Port'],
                    'Description': row['Description'],
                    'Solution': row['Solution']
                }
            else:
                grouped_rows[key]['Host:Port'] += f"\n{row['Host:Port']}"
                grouped_rows[key]['Description'] += f"\n{row['Description']}"
                grouped_rows[key]['Solution'] += f"\n{row['Solution']}"

        for key, value in grouped_rows.items():
            # Не совсем понял что значит "cлипляются", пока что оставлю так :)
            value['Name'] = f"{value['Name']} ({value['Risk Factor']})"

        risk_factor_priority = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}

        sorted_rows = sorted(grouped_rows.values(), key=lambda x: risk_factor_priority[x['Risk Factor']])

        with open(output_file_path, 'w', newline='') as outfile:
            fieldnames = ['Name', 'Risk Factor', 'Host:Port', 'Description', 'Solution']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in sorted_rows:
                writer.writerow(row)

        return Response({"message": f"CSV файл был успешно обработан и сохранен (Путь к файлу: {output_file_path})"})
