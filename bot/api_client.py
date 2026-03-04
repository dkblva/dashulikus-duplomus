import aiohttp
import asyncio
import ssl
from typing import Optional, List, Dict, Any
from config import API_BASE_URL, API_TIMEOUT

class APIClient:
    """Async HTTP client for FormAPI integration"""
    
    def __init__(self, base_url: str = API_BASE_URL, timeout: int = API_TIMEOUT):
        self.base_url = base_url
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session: Optional[aiohttp.ClientSession] = None
        # Создаем SSL context который не проверяет сертификаты (для localhost)
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
    
    async def connect(self):
        """Initialize session"""
        if self.session is None:
            connector = aiohttp.TCPConnector(ssl=self.ssl_context)
            self.session = aiohttp.ClientSession(timeout=self.timeout, connector=connector)
    
    async def disconnect(self):
        """Close session"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[Any, Any]]:
        """Make HTTP request"""
        try:
            await self.connect()
            url = f"{self.base_url}/{endpoint}"
            
            print(f"🔗 API Request: {method} {url}")
            
            async with self.session.request(method, url, ssl=self.ssl_context, **kwargs) as response:
                print(f"✅ API Response: {response.status}")
                
                if response.status in [200, 201]:
                    try:
                        return await response.json()
                    except:
                        return {"status": "success"}
                elif response.status == 204:
                    return {"status": "success"}
                else:
                    text = await response.text()
                    print(f"❌ API Error {response.status}: {text}")
                    return {"error": f"API Error {response.status}: {text}"}
        except asyncio.TimeoutError:
            print(f"⏱️ API Timeout")
            return {"error": "Timeout: API не ответил"}
        except Exception as e:
            print(f"❌ API Exception: {str(e)}")
            return {"error": f"Error: {str(e)}"}
    
    # ==================== Applications ====================
    
    async def get_applications(self) -> Optional[List[Dict]]:
        """Get all applications"""
        result = await self._request("GET", "api/applications")
        return result if isinstance(result, list) else None
    
    async def get_application(self, app_id: str) -> Optional[Dict]:
        """Get application by ID"""
        result = await self._request("GET", f"api/applications/{app_id}")
        return result if isinstance(result, dict) and "id" in result else None
    
    async def create_application(self, data: Dict) -> Optional[Dict]:
        """Create new application"""
        return await self._request("POST", "api/applications", json=data)
    
    async def update_application(self, app_id: str, data: Dict) -> Optional[Dict]:
        """Update application"""
        return await self._request("PUT", f"api/applications/{app_id}", json=data)
    
    async def delete_application(self, app_id: str) -> Optional[Dict]:
        """Delete application"""
        return await self._request("DELETE", f"api/applications/{app_id}")
    
    # ==================== Sphere Activity ====================
    
    async def get_spheres(self) -> Optional[List[Dict]]:
        """Get all sphere activities"""
        result = await self._request("GET", "api/sphereActivity")
        return result if isinstance(result, list) else None
    
    async def get_sphere(self, sphere_id: str) -> Optional[Dict]:
        """Get sphere by ID"""
        result = await self._request("GET", f"api/sphereActivity/{sphere_id}")
        return result if isinstance(result, dict) else None
    
    async def create_sphere(self, name: str) -> Optional[Dict]:
        """Create new sphere"""
        data = {"nameSphere": name}
        return await self._request("POST", "api/sphereActivity", json=data)
    
    async def update_sphere(self, sphere_id: str, name: str) -> Optional[Dict]:
        """Update sphere"""
        data = {"nameSphere": name}
        return await self._request("PUT", f"api/sphereActivity/{sphere_id}", json=data)
    
    async def delete_sphere(self, sphere_id: str) -> Optional[Dict]:
        """Delete sphere"""
        return await self._request("DELETE", f"api/sphereActivity/{sphere_id}")
    
    # ==================== Type Activity ====================
    
    async def get_types(self) -> Optional[List[Dict]]:
        """Get all type activities"""
        result = await self._request("GET", "api/typeActivity")
        return result if isinstance(result, list) else None
    
    async def get_type(self, type_id: str) -> Optional[Dict]:
        """Get type by ID"""
        result = await self._request("GET", f"api/typeActivity/{type_id}")
        return result if isinstance(result, dict) else None
    
    async def create_type(self, name: str) -> Optional[Dict]:
        """Create new type"""
        data = {"nameType": name}
        return await self._request("POST", "api/typeActivity", json=data)
    
    async def update_type(self, type_id: str, name: str) -> Optional[Dict]:
        """Update type"""
        data = {"nameType": name}
        return await self._request("PUT", f"api/typeActivity/{type_id}", json=data)
    
    async def delete_type(self, type_id: str) -> Optional[Dict]:
        """Delete type"""
        return await self._request("DELETE", f"api/typeActivity/{type_id}")
    
    # ==================== Tariffs ====================
    
    async def get_tariffs(self) -> Optional[List[Dict]]:
        """Get all tariffs"""
        result = await self._request("GET", "api/tarif")
        return result if isinstance(result, list) else None
    
    async def get_tariff(self, tarif_id: str) -> Optional[Dict]:
        """Get tariff by ID"""
        result = await self._request("GET", f"api/tarif/{tarif_id}")
        return result if isinstance(result, dict) else None
    
    async def create_tariff(self, name: str, description: str, price: int) -> Optional[Dict]:
        """Create new tariff"""
        data = {
            "name": name,
            "description": description,
            "price": price
        }
        return await self._request("POST", "api/tarif", json=data)
    
    async def update_tariff(self, tarif_id: str, data: Dict) -> Optional[Dict]:
        """Update tariff"""
        return await self._request("PUT", f"api/tarif/{tarif_id}", json=data)
    
    async def delete_tariff(self, tarif_id: str) -> Optional[Dict]:
        """Delete tariff"""
        return await self._request("DELETE", f"api/tarif/{tarif_id}")
    
    # ==================== Solutions ====================
    
    async def get_solutions(self) -> Optional[List[Dict]]:
        """Get all solutions"""
        result = await self._request("GET", "api/solution")
        return result if isinstance(result, list) else None
    
    async def get_solution(self, solution_id: str) -> Optional[Dict]:
        """Get solution by ID"""
        result = await self._request("GET", f"api/solution/{solution_id}")
        return result if isinstance(result, dict) else None
    
    async def create_solution(self, app_id: str, tarif_id: str, description: str) -> Optional[Dict]:
        """Create new solution"""
        data = {
            "idApplication": app_id,
            "idTarif": tarif_id,
            "description": description
        }
        return await self._request("POST", "api/solution", json=data)
    
    async def update_solution(self, solution_id: str, data: Dict) -> Optional[Dict]:
        """Update solution"""
        return await self._request("PUT", f"api/solution/{solution_id}", json=data)
    
    async def delete_solution(self, solution_id: str) -> Optional[Dict]:
        """Delete solution"""
        return await self._request("DELETE", f"api/solution/{solution_id}")
    
    async def get_solution_by_app(self, app_id: str) -> Optional[Dict]:
        """Get solution by application ID"""
        solutions = await self.get_solutions()
        if solutions:
            for sol in solutions:
                if sol.get("idApplication") == app_id:
                    return sol
        return None


# Global client instance
client = APIClient()
