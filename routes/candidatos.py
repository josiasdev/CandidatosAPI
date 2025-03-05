from fastapi import APIRouter, HTTPException, Query, Request, status, Depends
from typing import Annotated
from models.candidato import CandidatoCreate, CandidatoBase, CandidatoPublic, CandidatoUpdate
from pymongo.collection import Collection
from pymongo import ReturnDocument
from utils.utils import validate_object_id

from schemas.candidato import candidato_entity_from_db, candidato_entities_from_db

ERROR_DETAIL = "Some error occurred: {e}"
NOT_FOUND = "Not found"

async def get_candidato_collection(request: Request) -> Collection:
    """Returns the candidato collection from MongoDB"""
    return request.app.database["candidato"]

CandidatoCollection = Annotated[Collection, Depends(get_candidato_collection)]

router = APIRouter()

@router.post("/", 
    response_description="Registers a new Candidato", 
    status_code=status.HTTP_201_CREATED, response_model=CandidatoCreate)
async def create_candidato(accident_collection: CandidatoCollection, accident: CandidatoCreate):
    try:
        accident_data = accident.model_dump()
        result = accident_collection.insert_one(accident_data)
        
        if (created := accident_collection.find_one({"_id": result.inserted_id})) is None:
            raise HTTPException(500, "Failed to create Candidato")
            
        return candidato_entity_from_db(created)
    except Exception as e:
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

# @router.get("/filter")
# async def filter_customers(
#     customer_collection: CustomerCollection,
#     customer_name: str | None = None,  
#     limit: int = 10, 
#     page: int = 1
# ):
#     query_filter = {}

#     if customer_name:
#         query_filter['first_name'] = {"$regex": customer_name, "$options": "i"}

#     skip = (page - 1) * limit

#     return customers_entity(customer_collection.find(query_filter).skip(skip).limit(limit).to_list())

@router.get("/", 
    response_description="Retrieves Candidatos", 
    response_model=list[CandidatoPublic])
async def read_candidatos(
    candidato_collection: CandidatoCollection,
    page: Annotated[int, Query(ge=1, description="Pagination offset starting at 1")] = 1,
    limit: Annotated[int, Query(le=100, ge=1, description="Items per page (1-100)")] = 100
):
    cursor = candidato_collection.find().skip((page - 1) * limit).limit(limit)
    return candidato_entities_from_db(cursor)

# @router.get("/count", response_description="Get total Accident count")
# async def read_accident_count(accident_collection: AccidentCollection):
#     try:
#         return {"count": accident_collection.count_documents({})}
#     except Exception as e:
#         raise HTTPException(500, detail=ERROR_DETAIL.format(e=e))

# @router.get("/{id}",
#     response_description="Retrieves Individual Accident by ID", 
#     response_model=AccidentPublic)
# async def read_accident(
#     accident_collection: AccidentCollection, 
#     id: str = Depends(validate_object_id)
# ):
#     try:
#         if (accident := accident_collection.find_one({"_id": id})) is None:
#             raise HTTPException(404, detail=NOT_FOUND)
#         return accident_entity_from_db(accident)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

# @router.patch("/{id}",
#     response_description="Partially updates an Accident", 
#     response_model=AccidentPublic)
# async def update_accident(
#     accident_collection: AccidentCollection, 
#     accident: AccidentUpdate,
#     id: str = Depends(validate_object_id)
# ):
#     try:
#         update_data = accident.model_dump(exclude_unset=True)
        
#         updated = accident_collection.find_one_and_update(
#             {"_id": id},
#             {"$set": update_data},
#             return_document=ReturnDocument.AFTER
#         )
        
#         if not updated:
#             raise HTTPException(404, detail=NOT_FOUND)
            
#         return accident_entity_from_db(updated)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

# @router.put("/{id}", 
#     response_description="Fully update an Accident", 
#     response_model=AccidentPublic)
# async def fully_update_accident(
#     accident_collection: AccidentCollection, 
#     accident: AccidentBase,
#     id: str = Depends(validate_object_id)
# ):
#     try:
#         update_data = accident.model_dump()
        
#         updated = accident_collection.find_one_and_update(
#             {"_id": id},
#             {"$set": update_data},
#             return_document=ReturnDocument.AFTER
#         )
        
#         if not updated:
#             raise HTTPException(404, detail=NOT_FOUND)
            
#         return accident_entity_from_db(updated)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

# @router.delete("/{id}",
#     response_description="Deletes an Accident")
# async def delete_accident(
#     accident_collection: AccidentCollection, 
#     id: str = Depends(validate_object_id)
# ):
#     try:
#         result = accident_collection.delete_one({"_id": id})
        
#         if result.deleted_count == 0:
#             raise HTTPException(404, detail=NOT_FOUND)
            
#         return {"status": "success", "message": "Accident deleted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))