# produce pixel cluster & rechits from digia
# 
# To go from pixel clusters to rechits
#
##############################################################################
import FWCore.ParameterSet.Config as cms
process = cms.Process("RecHitTest")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
# select one of these
#process.load("Configuration.StandardSequences.GeometryRecoDB_cff") # works for MC & data
#process.load('Configuration.Geometry.GeometryExtended2017Reco_cff')
process.load("Configuration.Geometry.GeometryRecoDB_cff")
#process.load("Configuration.Geometry.GeometryReco_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("Configuration.StandardSequences.Services_cff")
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
# to use no All 
# Choose the global tag here:
# 2012
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run1_data', '')
#process.GlobalTag.globaltag = autoCond['run1_data']
#process.GlobalTag.globaltag = 'GR_R_73_V0A'
# 2015
#process.GlobalTag.globaltag = autoCpnd['run2_data']
# 2015
#process.GlobalTag.globaltag = 'GR_P_V49::All'
# 2016
#process.GlobalTag.globaltag = '80X_dataRun2_Prompt_v8' # for 272
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2017_realistic', '')

#process.GlobalTag.globaltag = 'PRE_R_71_V3'


# clusterizer & rechits 
#process.load("RecoLocalTracker.Configuration.RecoLocalTracker_cff")
# or use this
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("RecoLocalTracker.SiPixelRecHits.PixelCPEESProducers_cff")
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

process.MessageLogger = cms.Service("MessageLogger",
    #debugModules = cms.untracked.vstring('SiPixelClusterizer'),
    debugModules = cms.untracked.vstring('SiPixelRecHitConverter'),
    destinations = cms.untracked.vstring('cout'),
#    destinations = cms.untracked.vstring("log","cout"),
    cout = cms.untracked.PSet(
#       threshold = cms.untracked.string('INFO')
        threshold = cms.untracked.string('WARNING')
#       threshold = cms.untracked.string('ERROR')
    )
    #log = cms.untracked.PSet(
     #   threshold = cms.untracked.string('DEBUG')
    #)
)
# get the files from DBS:
process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
# 'file:tracks.root'
# 'file:/afs/cern.ch/work/d/dkotlins/public/MC/mu/pt100_71_pre7/tracks/tracks2_mc71.root'
# 'file:/afs/cern.ch/work/d/dkotlins/public/MC/mu/pt100_71_pre7/rechits/rechits2_mc71.root'
#2017
#'/store/relval/CMSSW_9_2_0/RelValZMM_13/GEN-SIM-RECO/PU25ns_91X_upgrade2017_realistic_v5-v1/10000/28E1F8B5-D63C-E711-A025-0CC47A4D768E.root'
#2016
'file:/afs/cern.ch/work/s/sdubey/data/9279A7C3-59ED-E511-95C8-0025905A60F8.root'
#'file:/afs/cern.ch/work/s/sdubey/data/RawToDigi/2EF61B7D-F216-E211-98C3-001D09F28D54.root'
#'file:/afs/cern.ch/work/s/sdubey/data/Raw_Data_Phase1/0216ABF7-19B1-E611-8786-0025905A60F8.root'
#'/store/mc/HG1504_HLT_Test/MajoranaNeutrinoToMuE_M-375_TuneZ2star_8TeV-alpgen/GEN-SIM/IntegrationTest1427988373HG1504_HLT_Test-v1/00000/103D51C3-1EDA-E411-83F2-02163E013038.root'
#"/store/express/Run2016B/ExpressPhysics/FEVT/Express-v2/000/274/314/00000/1A57B62A-4328-E611-9D78-02163E01339F.root",
#'/store/express/Run2016B/ExpressPhysics/FEVT/Express-v2/000/273/150/00000/0E6AF5CF-CC17-E611-B10E-02163E014705.root'
  )
)

#process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange('204217:60- 204217:9999')#('274314:97-274314:9999')

# a service to use root histos
process.TFileService = cms.Service("TFileService",
    fileName = cms.string('histo.root')
)


# DB stuff 
# GenError
useLocalDB = False
if useLocalDB :
    process.DBReaderFrontier = cms.ESSource("PoolDBESSource",
     DBParameters = cms.PSet(
         messageLevel = cms.untracked.int32(0),
         authenticationPath = cms.untracked.string('')
     ),
     toGet = cms.VPSet(
 	 cms.PSet(
          record = cms.string('SiPixelGenErrorDBObjectRcd'),
#          tag = cms.string('SiPixelGenErrorDBObject38TV10')
          tag = cms.string('SiPixelGenErrorDBObject_38T_v1_mc')
 	 ),
 	),
#     connect = cms.string('sqlite_file:siPixelGenErrors38T.db')
#     connect = cms.string('frontier://FrontierProd/CMS_COND_PIXEL_000')
     connect = cms.string('frontier://FrontierPrep/CMS_COND_PIXEL')
    ) # end process
    process.myprefer = cms.ESPrefer("PoolDBESSource","DBReaderFrontier")
# endif

useLocalDB2 = False
if useLocalDB2 :
    process.DBReaderFrontier2 = cms.ESSource("PoolDBESSource",
     DBParameters = cms.PSet(
         messageLevel = cms.untracked.int32(0),
         authenticationPath = cms.untracked.string('')
     ),
     toGet = cms.VPSet(
 		cms.PSet(
 			record = cms.string("SiPixelTemplateDBObjectRcd"),
 			tag = cms.string("SiPixelTemplateDBObject38TV10")
# 			tag = cms.string("SiPixelTemplateDBObject38Tv21")
 		),
 	),
     connect = cms.string('sqlite_file:siPixelTemplates38T.db')
#     connect = cms.string('frontier://FrontierPrep/CMS_COND_PIXEL')
#     connect = cms.string('frontier://FrontierProd/CMS_COND_31X_PIXEL')
    ) # end process
    process.myprefer2 = cms.ESPrefer("PoolDBESSource","DBReaderFrontier2")
# endif
 
#process.PoolDBESSource = cms.ESSource("PoolDBESSource",
#    BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
#    DBParameters = cms.PSet(
#        messageLevel = cms.untracked.int32(0),
#        authenticationPath = cms.untracked.string('')
#    ),
#    timetype = cms.string('runnumber'),
#    toGet = cms.VPSet(cms.PSet(
#        record = cms.string('SiPixelQualityRcd'),
#        tag = cms.string('SiPixelBadModule_test')
#    )),
#    connect = cms.string('sqlite_file:test.db')
#)
# To use a test DB instead of the official pixel object DB tag: 
#process.customDead = cms.ESSource("PoolDBESSource", process.CondDBSetup, connect = cms.string('sqlite_file:/afs/cern.ch/user/v/vesna/Digitizer/dead_20100901.db'), toGet = cms.VPSet(cms.PSet(record = cms.string('SiPixelQualityRcd'), tag = cms.string('dead_20100901'))))
#process.es_prefer_customDead = cms.ESPrefer("PoolDBESSource","customDead")


process.o1 = cms.OutputModule("PoolOutputModule",
                              outputCommands = cms.untracked.vstring('drop *','keep *_*_*_RecHitTest'),
            fileName = cms.untracked.string('file:rechits.root')
#            fileName = cms.untracked.string('file:/afs/cern.ch/work/d/dkotlins/public/MC/mu/pt100_71_pre7/rechits/rechits2_mc71.root')
)

# My 
# modify clusterie parameters (just an example)
#process.siPixelClusters.ClusterThreshold = 4000.0

# read rechits
process.analysis = cms.EDAnalyzer("ReadPixelRecHit",
    Verbosity = cms.untracked.bool(True),
    src = cms.InputTag("siPixelRecHits"),
)

# only rechits
process.p1 = cms.Path(process.siPixelRecHits)
#process.p1 = cms.Path(process.siPixelRecHits*process.analysis)

# save output 
process.outpath = cms.EndPath(process.o1)
