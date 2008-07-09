#! /bin/env cmsRun

import FWCore.ParameterSet.Config as cms

process = cms.Process("Geometry")

# random number generator service for these modules
process.load("SimTracker.TrackerMaterialAnalysis.randomNumberGeneratorService_cfi")

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.load("SimTracker.TrackerMaterialAnalysis.double10GeVPions_cfi")

# gaussian Vertex Smearing
process.load("Configuration.StandardSequences.VtxSmearedGauss_cff")

# detector simulation (Geant4-based) with tracking material accounting 
process.load("SimTracker.TrackerMaterialAnalysis.trackingMaterialProducer_cff")

process.MessageLogger = cms.Service("MessageLogger",
    cout = cms.untracked.PSet(
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        FwkJob = cms.untracked.PSet(    # but FwkJob category - those unlimitted

            limit = cms.untracked.int32(-1)
        )
    ),
    categories = cms.untracked.vstring('FwkJob'),
    destinations = cms.untracked.vstring('cout')
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)
process.out = cms.OutputModule("PoolOutputModule",
    outputCommands = cms.untracked.vstring(
        'drop *',                                                       # drop all objects
        'keep MaterialAccountingTracks_trackingMaterialProducer_*_*'),  # but the material accounting informations
    fileName = cms.untracked.string('file:material.root')
)

process.p = cms.Path(process.VtxSmeared*process.trackingMaterialProducer)
process.outpath = cms.EndPath(process.out)
