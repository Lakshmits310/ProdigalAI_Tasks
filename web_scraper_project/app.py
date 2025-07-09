from flask import Flask, render_template, jsonify, send_file
from scrapers import DataHandler
import os
import json
import traceback

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scrape')
def scrape_data():
    try:
        handler = DataHandler()

        # Scraping and Saving
        handler.collect_data()
        handler.save_all_sources_json_csv()
        handler.save_combined_json()
        handler.save_combined_csv()

        # Generate scraping summary
        report = handler.generate_summary_report()

        return jsonify({
            "status": "success",
            "message": "Data scraped and saved successfully ✅",
            "report": report
        })

    except Exception as e:
        print("❌ Scraping Error:", traceback.format_exc())
        return jsonify({
            "status": "error",
            "message": f"Error during scraping: {str(e)}"
        }), 500


@app.route('/data')
def get_data():
    filepath = 'data/combined_data.json'
    if not os.path.exists(filepath):
        return jsonify({"error": "❗ Data not found. Please run `/scrape` first."}), 404

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return jsonify(data)


@app.route('/download/<file_type>')
def download_data(file_type):
    if file_type == 'json':
        filepath = 'data/combined_data.json'
    elif file_type == 'csv':
        filepath = 'data/combined_data.csv'
    else:
        return jsonify({"error": "❌ Invalid file type"}), 400

    if not os.path.exists(filepath):
        return jsonify({"error": "❗ File not found. Please run `/scrape` first."}), 404

    return send_file(filepath, as_attachment=True)


@app.route('/report')
def get_report():
    filepath = 'data/scraping_report.json'
    if not os.path.exists(filepath):
        return jsonify({"error": "❗ Report not found. Please run `/scrape` first."}), 404

    with open(filepath, 'r', encoding='utf-8') as f:
        report = json.load(f)

    return jsonify(report)


if __name__ == '__main__':
    # Run on all addresses so it’s accessible via local IP (for demo)
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
