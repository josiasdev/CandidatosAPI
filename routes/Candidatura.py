from fastapi import APIRouter, HTTPException, Query, Request, status, Depends
from typing import Annotated
from models.candidatura import CandidaturaBase, CandidaturaCreate, CandidaturaPublic, CandidaturaUpdate
from pymongo.collection import Collection
from pymongo import ReturnDocument
from utils.utils import validate_object_id
from schemas.Candidatura import candidatura_entity_from_db, candidatura_entities_from_db
import logging

ERROR_DETAIL = "Some error occurred: {e}"
NOT_FOUND = "Not found"

async def get_candidatura_collection(request: Request) -> Collection:
    """Returns the candidatura collection from MongoDB"""
    return request.app.database["candidatura"]

CandidaturaCollection = Annotated[Collection, Depends(get_candidatura_collection)]
logger = logging.getLogger("app_logger")

router = APIRouter()

@router.post("/",response_description="Registers a new Candidatura",status_code=status.HTTP_201_CREATED, response_model=CandidaturaPublic)
async def create_candidatura(candidatura_collection: CandidaturaCollection, candidatura: CandidaturaCreate):
    try:
        candidatura_data = candidatura.model_dump()
        result = candidatura_collection.insert_one(candidatura_data)
        
        if (created := candidatura_collection.find_one({"_id": result.inserted_id})) is None:
            raise HTTPException(500, "Failed to create Candidatura")
        
        logger.info(f"Candidatura created with id: {result.inserted_id}")
        return candidatura_entity_from_db(created)
    except Exception as e:
        logger.error(f"Error creating Candidatura: {e}")
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

@router.get("/", response_description="Retrieves Candidaturas", response_model=list[CandidaturaPublic])
async def read_candidaturas(
    candidatura_collection: CandidaturaCollection,
    page: Annotated[int, Query(ge=1, description="Pagination offset starting at 1")] = 1,
    limit: Annotated[int, Query(le=100, ge=1, description="Items per page (1-100)")] = 100
):
    try:
        cursor = candidatura_collection.find().skip((page - 1) * limit).limit(limit)
        logger.info(f"Retrieved Candidaturas with pagination: page={page}, limit={limit}")

        candidatos = list(cursor)  
        print("[DEBUG] Dados brutos do MongoDB:", candidatos)  
        
        return candidatura_entities_from_db(candidatos)
    except Exception as e:
        logger.error(f"Error retrieving Candidaturas: {e}")
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

@router.get("/count", response_description="Get total Candidatura count")
async def read_candidatura_count(candidatura_collection: CandidaturaCollection):
    try:
        count = candidatura_collection.count_documents({})
        logger.info(f"Total Candidatura count: {count}")
        return {"count": count}
    except Exception as e:
        logger.error(f"Error getting Candidatura count: {e}")
        raise HTTPException(500, detail=ERROR_DETAIL.format(e=e))

@router.get("/{id}",
    response_description="Retrieves Individual Candidatura by ID", 
    response_model=CandidaturaPublic)
async def read_candidatura(
    candidatura_collection: CandidaturaCollection, 
    id: str = Depends(validate_object_id)
):
    try:
        if (candidatura := candidatura_collection.find_one({"_id": id})) is None:
            raise HTTPException(404, detail=NOT_FOUND)
        logger.info(f"Retrieved Candidatura with id: {id}")
        return candidatura_entity_from_db(candidatura)
    except Exception as e:
        logger.error(f"Error retrieving Candidatura with id {id}: {e}")
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

@router.patch("/{id}",
    response_description="Partially updates a Candidatura", 
    response_model=CandidaturaPublic)
async def update_candidatura(
    candidatura_collection: CandidaturaCollection, 
    candidatura: CandidaturaUpdate,
    id: str = Depends(validate_object_id)
):
    try:
        update_data = candidatura.model_dump(exclude_unset=True)
        
        updated = candidatura_collection.find_one_and_update(
            {"_id": id},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )
        
        if not updated:
            raise HTTPException(404, detail=NOT_FOUND)
        
        logger.info(f"Partially updated Candidatura with id: {id}")
        return candidatura_entity_from_db(updated)
    except Exception as e:
        logger.error(f"Error partially updating Candidatura with id {id}: {e}")
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

@router.put("/{id}", 
    response_description="Fully update a Candidatura", 
    response_model=CandidaturaPublic)
async def fully_update_candidatura(
    candidatura_collection: CandidaturaCollection, 
    candidatura: CandidaturaBase,
    id: str = Depends(validate_object_id)
):
    try:
        update_data = candidatura.model_dump()
        
        updated = candidatura_collection.find_one_and_update(
            {"_id": id},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )
        
        if not updated:
            raise HTTPException(404, detail=NOT_FOUND)
        
        logger.info(f"Fully updated Candidatura with id: {id}")
        return candidatura_entity_from_db(updated)
    except Exception as e:
        logger.error(f"Error fully updating Candidatura with id {id}: {e}")
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

@router.delete("/{id}",
    response_description="Deletes a Candidatura")
async def delete_candidatura(
    candidatura_collection: CandidaturaCollection, 
    id: str = Depends(validate_object_id)
):
    try:
        result = candidatura_collection.delete_one({"_id": id})
        
        if result.deleted_count == 0:
            raise HTTPException(404, detail=NOT_FOUND)
        
        logger.info(f"Deleted Candidatura with id: {id}")
        return {"status": "success", "message": "Candidatura deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting Candidatura with id {id}: {e}")
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))