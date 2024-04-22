from aiohttp import web
import asyncio
import subprocess

TOKEN = '9999'

# Token checking middleware
@web.middleware
async def token_check_middleware(request, handler):
    token = request.query.get('token')  # Get token from query parameters
    if token != TOKEN:
        return web.json_response({'error': 'Unauthorized'}, status=401)
    return await handler(request)

# Run Docker Compose command asynchronously
async def run_docker_compose_command(service, command):
    process = await asyncio.create_subprocess_exec(
        'docker-compose', command, service,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    if process.returncode == 0:
        return f'{service} {command.replace("docker-compose", "").strip()}ed successfully', stdout.decode().strip()
    else:
        return f'Error {command.replace("docker-compose", "").strip()}ing {service}: {stderr.decode()}', None

# Handler functions for starting, stopping, and restarting services
async def start(request):
    service = request.match_info['service']
    response, _ = await run_docker_compose_command(service, 'start')
    return web.json_response({'status': response})

async def stop(request):
    service = request.match_info['service']
    response, _ = await run_docker_compose_command(service, 'stop')
    return web.json_response({'status': response})

async def restart(request):
    service = request.match_info['service']
    response, _ = await run_docker_compose_command(service, 'restart')
    return web.json_response({'status': response})

async def status(request):
    service = request.match_info['service']
    response, output = await run_docker_compose_command(service, 'ps')
    if output:
        return web.json_response({'status': 'Service running', 'details': output})
    else:
        return web.json_response({'status': response})

# Application setup with middleware
app = web.Application(middlewares=[token_check_middleware])
app.router.add_get('/start/{service}', start)
app.router.add_get('/stop/{service}', stop)
app.router.add_get('/restart/{service}', restart)
app.router.add_get('/status/{service}', status)  # Adding the status endpoint

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=50000)
