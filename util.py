from datetime import datetime

def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"

def time_ago_str(datetime_obj):
    timedelta = datetime.now() - datetime_obj
    return_str = ''
    if timedelta.days > 30:
        return_str =  f'{timedelta.days * 30} month'
        if timedelta.days > 60:
            return_str += 's'
    elif timedelta.days > 0:
        return_str =  f'{timedelta.days} day'
        if timedelta.days > 1:
            return_str += 's'
    elif timedelta.hours > 0:
        return_str =  f'{timedelta.hours} hour'
        if timedelta.hours > 1:
            return_str += 's'
    elif timedelta.minutes > 0:
        return_str =  f'{timedelta.minutes} minute'
        if timedelta.minutes > 1:
            return_str += 's'        
    elif timedelta.seconds > 0:
        return_str =  f'{timedelta.seconds} second'
        if timedelta.seconds > 1:
            return_str += 's'       
    
    return f'{return_str} ago'

def get_progress_bar(progress, bar_length=13):
    bar_increment = 1.0 / bar_length
    bar_value = 0.0
    bar_str = ''
    
    for bar_num in range(0, bar_length):
        if (bar_value) < progress - bar_increment:
            bar_str += '▰'
        else:
            bar_str += '▱'
        
        bar_value += bar_increment
    
    return bar_str
