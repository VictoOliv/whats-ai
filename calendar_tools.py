import os
import pickle
from datetime import datetime, timedelta
from typing import Optional, List
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langchain_core.tools import tool

# Se modificar esses escopos, delete o arquivo token.pickle
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Obtém o serviço do Google Calendar autenticado."""
    creds = None
    
    # O arquivo token.pickle armazena os tokens de acesso e refresh do usuário
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # Se não há credenciais válidas disponíveis, fazer login do usuário
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError(
                    "Arquivo 'credentials.json' não encontrado. "
                    "Faça o download das credenciais OAuth 2.0 do Google Cloud Console."
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Salva as credenciais para a próxima execução
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('calendar', 'v3', credentials=creds)


@tool
def list_calendar_events(
    max_results: int = 10,
    days_ahead: int = 7
) -> str:
    """
    Lista os próximos eventos do Google Calendar.
    
    Args:
        max_results: Número máximo de eventos a retornar (padrão: 10)
        days_ahead: Número de dias à frente para buscar eventos (padrão: 7)
    
    Returns:
        String formatada com a lista de eventos ou mensagem se não houver eventos
    """
    try:
        service = get_calendar_service()
        
        # Busca eventos a partir de agora
        now = datetime.utcnow().isoformat() + 'Z'
        time_max = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=time_max,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            return f'Nenhum evento encontrado nos próximos {days_ahead} dias.'
        
        result = [f'Próximos {len(events)} eventos:']
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event.get('summary', 'Sem título')
            
            # Formata a data/hora
            try:
                if 'T' in start:
                    dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                    formatted_date = dt.strftime('%d/%m/%Y às %H:%M')
                else:
                    dt = datetime.fromisoformat(start)
                    formatted_date = dt.strftime('%d/%m/%Y (dia inteiro)')
            except:
                formatted_date = start
            
            result.append(f'- {summary} - {formatted_date}')
        
        return '\n'.join(result)
        
    except HttpError as error:
        return f'Erro ao buscar eventos: {error}'
    except Exception as e:
        return f'Erro: {str(e)}'


@tool
def create_calendar_event(
    summary: str,
    start_datetime: str,
    end_datetime: str,
    description: Optional[str] = None,
    location: Optional[str] = None
) -> str:
    """
    Cria um novo evento no Google Calendar.
    
    Args:
        summary: Título do evento
        start_datetime: Data/hora de início no formato ISO (ex: "2024-01-15T10:00:00-03:00")
        end_datetime: Data/hora de término no formato ISO (ex: "2024-01-15T11:00:00-03:00")
        description: Descrição do evento (opcional)
        location: Localização do evento (opcional)
    
    Returns:
        String confirmando a criação do evento ou mensagem de erro
    """
    try:
        service = get_calendar_service()
        
        event = {
            'summary': summary,
            'start': {
                'dateTime': start_datetime,
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': end_datetime,
                'timeZone': 'America/Sao_Paulo',
            },
        }
        
        if description:
            event['description'] = description
        
        if location:
            event['location'] = location
        
        event = service.events().insert(calendarId='primary', body=event).execute()
        
        return f'Evento criado com sucesso: {summary}\nLink: {event.get("htmlLink")}'
        
    except HttpError as error:
        return f'Erro ao criar evento: {error}'
    except Exception as e:
        return f'Erro: {str(e)}'


@tool
def search_calendar_events(
    query: str,
    max_results: int = 10
) -> str:
    """
    Busca eventos no Google Calendar por palavra-chave.
    
    Args:
        query: Texto para buscar nos eventos
        max_results: Número máximo de resultados (padrão: 10)
    
    Returns:
        String formatada com os eventos encontrados ou mensagem se não houver resultados
    """
    try:
        service = get_calendar_service()
        
        # Busca eventos a partir de 30 dias atrás
        time_min = (datetime.utcnow() - timedelta(days=30)).isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime',
            q=query
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            return f'Nenhum evento encontrado com "{query}".'
        
        result = [f'Eventos encontrados ({len(events)}):']
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event.get('summary', 'Sem título')
            
            # Formata a data/hora
            try:
                if 'T' in start:
                    dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                    formatted_date = dt.strftime('%d/%m/%Y às %H:%M')
                else:
                    dt = datetime.fromisoformat(start)
                    formatted_date = dt.strftime('%d/%m/%Y (dia inteiro)')
            except:
                formatted_date = start
            
            result.append(f'- {summary} - {formatted_date}')
        
        return '\n'.join(result)
        
    except HttpError as error:
        return f'Erro ao buscar eventos: {error}'
    except Exception as e:
        return f'Erro: {str(e)}'


@tool
def delete_calendar_event(event_id: str) -> str:
    """
    Deleta um evento do Google Calendar.
    
    Args:
        event_id: ID do evento a ser deletado
    
    Returns:
        String confirmando a deleção ou mensagem de erro
    """
    try:
        service = get_calendar_service()
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        return f'Evento deletado com sucesso.'
        
    except HttpError as error:
        return f'Erro ao deletar evento: {error}'
    except Exception as e:
        return f'Erro: {str(e)}'


# Lista de todas as tools disponíveis
CALENDAR_TOOLS = [
    list_calendar_events,
    create_calendar_event,
    search_calendar_events,
    delete_calendar_event,
]

