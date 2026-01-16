from supabase import create_client, Client
from config import get_settings
import psycopg2
from psycopg2 import pool
from typing import Optional

settings = get_settings()


class SupabaseClient:
    """Singleton Supabase client for API operations"""
    _instance: Optional[Client] = None
    
    @classmethod
    def get_client(cls) -> Client:
        if cls._instance is None:
            cls._instance = create_client(
                settings.supabase_url,
                settings.supabase_service_role_key
            )
        return cls._instance


class PostgresPool:
    """PostgreSQL connection pool for direct database operations (RAG, vectors)"""
    _pool: Optional[pool.SimpleConnectionPool] = None
    
    @classmethod
    def get_pool(cls) -> pool.SimpleConnectionPool:
        if cls._pool is None:
            cls._pool = pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                dsn=settings.database_url
            )
        return cls._pool
    
    @classmethod
    def get_connection(cls):
        """Get a connection from the pool"""
        return cls.get_pool().getconn()
    
    @classmethod
    def return_connection(cls, conn):
        """Return a connection to the pool"""
        cls.get_pool().putconn(conn)


# Convenience functions
def get_supabase() -> Client:
    """Get Supabase client instance"""
    return SupabaseClient.get_client()


def get_db_connection():
    """Get PostgreSQL connection from pool"""
    return PostgresPool.get_connection()


def return_db_connection(conn):
    """Return PostgreSQL connection to pool"""
    PostgresPool.return_connection(conn)
