import traceback


# import exception_logger


def log_traceback(ex: Exception):
    _tb_lines = traceback.format_exception(ex.__class__, ex, ex.__traceback__)
    _tb_text = ''.join(_tb_lines)

    lines = _tb_text.split('Traceback')
    print("Traceback" + lines[len(lines) - 1])

    # exception_logger.log(_tb_text)
