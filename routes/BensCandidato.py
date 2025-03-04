from fastapi import APIRouter, HTTPException, Query, Request, status, Depends
from typing import Annotated
from models.BensCandidato import BensCandidatoBase, BensCandidatoCreate, BensCandidatoPublic, BensCandidatoUpdate
from pymongo.collection import Collection
from pymongo import ReturnDocument
from utils.utils import validate_object_id
from schemas.BensCandidato import bens_candidato_entity_from_db, bens_candidato_entities_from_db
import logging

ERROR_DETAIL = "Some error occurred: {e}"
NOT_FOUND = "Not found"

async def get_bens_candidato_collection(request: Request) -> Collection:
    """Returns the bens_candidato collection from MongoDB"""
    return request.app.database["bens_candidato"]

BensCandidatoCollection = Annotated[Collection, Depends(get_bens_candidato_collection)]
logger = logging.getLogger("app_logger")

router = APIRouter()

@router.post("/", 
    response_description="Registers a new BensCandidato", 
    status_code=status.HTTP_201_CREATED, response_model=BensCandidatoPublic)
async def create_bens_candidato(bens_candidato_collection: BensCandidatoCollection, bens_candidato: BensCandidatoCreate):
    try:
        bens_candidato_data = bens_candidato.model_dump()
        result = bens_candidato_collection.insert_one(bens_candidato_data)
        
        if (created := bens_candidato_collection.find_one({"_id": result.inserted_id})) is None:
            raise HTTPException(500, "Failed to create BensCandidato")
        
        logger.info(f"BensCandidato created with id: {result.inserted_id}")
        return bens_candidato_entity_from_db(created)
    except Exception as e:
        logger.error(f"Error creating BensCandidato: {e}")
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

@router.get("/", 
    response_description="Retrieves BensCandidatos", 
    response_model=list[BensCandidatoPublic])
async def read_bens_candidatos(
    bens_candidato_collection: BensCandidatoCollection,
    page: Annotated[int, Query(ge=1, description="Pagination offset starting at 1")] = 1,
    limit: Annotated[int, Query(le=100, ge=1, description="Items per page (1-100)")] = 100
):
    try:
        cursor = bens_candidato_collection.find().skip((page - 1) * limit).limit(limit)
        logger.info(f"Retrieved BensCandidatos with pagination: page={page}, limit={limit}")
        return bens_candidato_entities_from_db(cursor)
    except Exception as e:
        logger.error(f"Error retrieving BensCandidatos: {e}")
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

@router.get("/count", response_description="Get total BensCandidato count")
async def read_bens_candidato_count(bens_candidato_collection: BensCandidatoCollection):
    try:
        count = bens_candidato_collection.count_documents({})
        logger.info(f"Total BensCandidato count: {count}")
        return {"count": count}
    except Exception as e:
        logger.error(f"Error getting BensCandidato count: {e}")
        raise HTTPException(500, detail=ERROR_DETAIL.format(e=e))

@router.get("/{id}",
    response_description="Retrieves Individual BensCandidato by ID", 
    response_model=BensCandidatoPublic)
async def read_bens_candidato(
    bens_candidato_collection: BensCandidatoCollection, 
    id: str = Depends(validate_object_id)
):
    try:
        if (bens_candidato := bens_candidato_collection.find_one({"_id": id})) is None:
            raise HTTPException(404, detail=NOT_FOUND)
        logger.info(f"Retrieved BensCandidato with id: {id}")
        return bens_candidato_entity_from_db(bens_candidato)
    except Exception as e:
        logger.error(f"Error retrieving BensCandidato with id {id}: {e}")
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

@router.patch("/{id}",
    response_description="Partially updates a BensCandidato", 
    response_model=BensCandidatoPublic)
async def update_bens_candidato(
    bens_candidato_collection: BensCandidatoCollection, 
    bens_candidato: BensCandidatoUpdate,
    id: str = Depends(validate_object_id)
):
    try:
        update_data = bens_candidato.model_dump(exclude_unset=True)
        
        updated = bens_candidato_collection.find_one_and_update(
            {"_id": id},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )
        
        if not updated:
            raise HTTPException(404, detail=NOT_FOUND)
        
        logger.info(f"Partially updated BensCandidato with id: {id}")
        return bens_candidato_entity_from_db(updated)
    except Exception as e:
        logger.error(f"Error partially updating BensCandidato with id {id}: {e}")
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

@router.put("/{id}", 
    response_description="Fully update a BensCandidato", 
    response_model=BensCandidatoPublic)
async def fully_update_bens_candidato(
    bens_candidato_collection: BensCandidatoCollection, 
    bens_candidato: BensCandidatoBase,
    id: str = Depends(validate_object_id)
):
    try:
        update_data = bens_candidato.model_dump()
        
        updated = bens_candidato_collection.find_one_and_update(
            {"_id": id},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )
        
        if not updated:
            raise HTTPException(404, detail=NOT_FOUND)
        
        logger.info(f"Fully updated BensCandidato with id: {id}")
        return bens_candidato_entity_from_db(updated)
    except Exception as e:
        logger.error(f"Error fully updating BensCandidato with id {id}: {e}")
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

@router.delete("/{id}",
    response_description="Deletes a BensCandidato")
async def delete_bens_candidato(
    bens_candidato_collection: BensCandidatoCollection, 
    id: str = Depends(validate_object_id)
):
    try:
        result = bens_candidato_collection.delete_one({"_id": id})
        
        if result.deleted_count == 0:
            raise HTTPException(404, detail=NOT_FOUND)
        
        logger.info(f"Deleted BensCandidato with id: {id}")
        return {"status": "success", "message": "BensCandidato deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting BensCandidato with id {id}: {e}")
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))