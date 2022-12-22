from datetime import datetime

def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0

    if unit in ['B', 'KB', 'MB']:
        decimal_places = 0

    return f"{size:.{decimal_places}f} {unit}"

def time_ago_str(datetime_obj):
    timedelta_obj = datetime.now() - datetime_obj
    return time_ago_timedelta_str(timedelta_obj)

def time_ago_timedelta_str(timedelta_obj, suffix=" ago"):
    return_str = ''

    hours, remainder = divmod(timedelta_obj.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if timedelta_obj.days > 30:
        return_str =  f'{timedelta_obj.days * 30} month'
        if timedelta_obj.days > 60:
            return_str += 's'
    elif timedelta_obj.days > 0:
        return_str =  f'{timedelta_obj.days} day'
        if timedelta_obj.days > 1:
            return_str += 's'
    elif hours > 0:
        return_str =  f'{hours} hour'
        if hours > 1:
            return_str += 's'
    elif minutes > 0:
        return_str =  f'{minutes} minute'
        if minutes > 1:
            return_str += 's'        
    elif seconds > 0:
        return_str =  f'{seconds} second'
        if seconds > 1:
            return_str += 's'       
    
    return f'{return_str}{suffix}'


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
