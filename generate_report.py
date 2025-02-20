import glob
import re
from jinja2 import Template

def parse_results():
    data = {
        'dates': [],
        'providers': set(),
        'ttft': {},
        'tbt': {}
    }
    
    # First pass: collect all dates and providers
    result_files = sorted(glob.glob('results_*.txt'))
    for file in result_files:
        date_str = file.split('_')[1].split('.')[0]
        data['dates'].append(date_str)
        
        with open(file, 'r') as f:
            lines = f.readlines()
        
        for line in lines[2:]:
            if line.strip():
                match = re.match(r'(\S+)\s+(\d+\.\d+)\s+(\d+\.\d+)', line.strip())
                if match:
                    provider = match.group(1)
                    data['providers'].add(provider)
    
    # Initialize data structures for each provider
    data['providers'] = sorted(list(data['providers']))
    for provider in data['providers']:
        data['ttft'][provider] = [0] * len(data['dates'])
        data['tbt'][provider] = [0] * len(data['dates'])
    
    # Second pass: fill in the data
    for idx, file in enumerate(result_files):
        with open(file, 'r') as f:
            lines = f.readlines()
        
        for line in lines[2:]:
            if line.strip():
                match = re.match(r'(\S+)\s+(\d+\.\d+)\s+(\d+\.\d+)', line.strip())
                if match:
                    provider, ttft, tbt = match.groups()
                    data['ttft'][provider][idx] = float(ttft)
                    data['tbt'][provider][idx] = float(tbt)
    
    return data

def generate_html():
    # Read template
    with open('template.html', 'r') as f:
        template = Template(f.read())
    
    # Parse results
    data = parse_results()
    
    # Generate HTML
    html = template.render(data=data)
    
    # Write output
    with open('docs/index.html', 'w') as f:
        f.write(html)

if __name__ == '__main__':
    generate_html()
