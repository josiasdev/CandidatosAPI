from fastapi import APIRouter, HTTPException, Query, Request, status, Depends
from typing import Annotated
from models.candidato import CandidatoCreate, CandidatoBase, CandidatoPublic, CandidatoUpdate
from pymongo.collection import Collection
from pymongo import ReturnDocument

from schemas.candidato import candidato_entity, candidato_entities

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
            
        return candidato_entity(created)
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
    return candidato_entities(cursor)

@router.get("/count", response_description="Get total Candidato count")
async def read_candidato_count(candidato_collection: CandidatoCollection):
    try:
        return {"count": candidato_collection.count_documents({})}
    except Exception as e:
        raise HTTPException(500, detail=ERROR_DETAIL.format(e=e))

@router.get("/{id}",
    response_description="Retrieves Individual Candidato by nr_titulo", 
    response_model=CandidatoPublic)
async def read_candidato(
    candidato_collection: CandidatoCollection, 
    id: int
):
    try:
        if (candidato := candidato_collection.find_one({"nr_titulo_eleitoral_candidato": id})) is None:
            raise HTTPException(404, detail=NOT_FOUND)
        return candidato_entity(candidato)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

@router.patch("/{id}",
    response_description="Partially updates an Candidato", 
    response_model=CandidatoPublic)
async def update_candidato(
    candidato_collection: CandidatoCollection, 
    candidato: CandidatoUpdate,
    id: int
):
    try:
        update_data = candidato.model_dump(exclude_unset=True)
        
        updated = candidato_collection.find_one_and_update(
            {"nr_titulo_eleitoral_candidato": id},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )
        
        if not updated:
            raise HTTPException(404, detail=NOT_FOUND)
            
        return candidato_entity(updated)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

@router.put("/{id}", 
    response_description="Fully update an Candidato", 
    response_model=CandidatoPublic)
async def fully_update_candidato(
    candidato_collection: CandidatoCollection, 
    candidato: CandidatoBase,
    id: int
):
    try:
        update_data = candidato.model_dump()
        
        updated = candidato_collection.find_one_and_update(
            {"nr_titulo_eleitoral_candidato": id},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )
        
        if not updated:
            raise HTTPException(404, detail=NOT_FOUND)
            
        return candidato_entity(updated)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

@router.delete("/{id}",
    response_description="Deletes an Candidato")
async def delete_candidato(
    candidato_collection: CandidatoCollection, 
    id: int
):
    try:
        result = candidato_collection.delete_one({"nr_titulo_eleitoral_candidato": id})
        
        if result.deleted_count == 0:
            raise HTTPException(404, detail=NOT_FOUND)
            
        return {"status": "success", "message": "Candidato deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))