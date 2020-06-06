

def paging(page, limit, obj):
    start = (int(page) - 1) * int(limit)
    end = start + int(limit)
    objs = obj[start:end]
    objs_count = obj.count()
    return {
        'objs': objs,
        'objs_count': objs_count
    }
