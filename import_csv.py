"""
CSV Import Tool for PCSO Lotto Data
Allows manual import of data from CSV files
"""
import csv
import json
from datetime import datetime
import sys

def import_csv_to_json(csv_file):
    """
    Import PCSO data from CSV file
    Expected CSV format:
    Game,Numbers,Date,Jackpot,Winners
    """
    results = []
    
    print(f"Importing data from {csv_file}...")
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Parse numbers
                numbers_str = row.get('Numbers', row.get('COMBINATIONS', ''))
                numbers = [int(n.strip()) for n in numbers_str.replace('-', ' ').split()]
                
                # Parse date
                date_str = row.get('Date', row.get('DRAW DATE', ''))
                try:
                    date_obj = datetime.strptime(date_str, '%m/%d/%Y')
                    date_formatted = date_obj.strftime('%Y-%m-%d')
                except:
                    try:
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                        date_formatted = date_str
                    except:
                        date_formatted = date_str
                
                # Parse jackpot
                jackpot_str = row.get('Jackpot', row.get('JACKPOT (PHP)', '0'))
                try:
                    jackpot = float(jackpot_str.replace('PHP', '').replace('₱', '').replace(',', '').strip())
                except:
                    jackpot = 0
                
                # Parse winners
                winners_str = row.get('Winners', row.get('WINNERS', '0'))
                try:
                    winners = int(winners_str.replace(',', '').strip())
                except:
                    winners = 0
                
                # Get game name and determine type
                game_name = row.get('Game', row.get('LOTTO GAME', '')).strip()
                game_type = extract_game_type(game_name)
                
                result = {
                    "game": game_name,
                    "game_type": game_type,
                    "date": date_formatted,
                    "numbers": numbers,
                    "jackpot": jackpot,
                    "winners": winners
                }
                
                results.append(result)
        
        print(f"Successfully imported {len(results)} records")
        
        # Save to JSON
        output_data = {
            "last_updated": datetime.now().isoformat(),
            "total_results": len(results),
            "source": "manual_csv_import",
            "results": results
        }
        
        with open('pcso_lotto_data.json', 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print("Data saved to pcso_lotto_data.json")
        
        # Generate statistics
        generate_statistics(results)
        
        return results
        
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found")
        return None
    except Exception as e:
        print(f"Error importing CSV: {e}")
        return None

def extract_game_type(game_name):
    """Extract game type from game name"""
    game_name_lower = game_name.lower()
    
    if '6/58' in game_name:
        return '6/58'
    elif '6/55' in game_name:
        return '6/55'
    elif '6/49' in game_name:
        return '6/49'
    elif '6/45' in game_name:
        return '6/45'
    elif '6/42' in game_name:
        return '6/42'
    elif '6d' in game_name_lower:
        return '6D'
    elif '4d' in game_name_lower:
        return '4D'
    elif '3d' in game_name_lower:
        if '2pm' in game_name_lower:
            return '3D-2PM'
        elif '5pm' in game_name_lower:
            return '3D-5PM'
        elif '9pm' in game_name_lower:
            return '3D-9PM'
        return '3D'
    elif '2d' in game_name_lower:
        if '2pm' in game_name_lower:
            return '2D-2PM'
        elif '5pm' in game_name_lower:
            return '2D-5PM'
        elif '9pm' in game_name_lower:
            return '2D-9PM'
        return '2D'
    else:
        return game_name

def generate_statistics(results):
    """Generate statistics from imported data"""
    stats = {
        "by_game": {},
        "total_draws": len(results)
    }
    
    for result in results:
        game_type = result["game_type"]
        
        if game_type not in stats["by_game"]:
            stats["by_game"][game_type] = {
                "count": 0,
                "game_name": result["game"],
                "number_frequency": {}
            }
        
        stats["by_game"][game_type]["count"] += 1
        
        # Count number frequency (only for 6-digit games)
        if game_type.startswith("6/"):
            for num in result["numbers"]:
                if str(num) not in stats["by_game"][game_type]["number_frequency"]:
                    stats["by_game"][game_type]["number_frequency"][str(num)] = 0
                stats["by_game"][game_type]["number_frequency"][str(num)] += 1
    
    # Sort frequency
    for game_type in stats["by_game"]:
        if stats["by_game"][game_type]["number_frequency"]:
            stats["by_game"][game_type]["number_frequency"] = dict(
                sorted(stats["by_game"][game_type]["number_frequency"].items(), 
                       key=lambda x: x[1], reverse=True)
            )
    
    with open('pcso_statistics.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    print("Statistics saved to pcso_statistics.json")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import_csv.py <csv_file>")
        print("\nExample CSV format:")
        print("Game,Numbers,Date,Jackpot,Winners")
        print("Ultra Lotto 6/58,35-37-14-01-43-12,12/16/2025,49500000,0")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    import_csv_to_json(csv_file)
    
    print("\nImport complete! You can now open dashboard.html to view the data.")
