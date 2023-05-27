#!/usr/bin/python

# This file generated by a program. do not edit.


import pycopia.XML.POM

attribN_1304866719271601641 = pycopia.XML.POM.XMLAttribute(u'n', 1, 12, None)


attribN_4095895239692176041 = pycopia.XML.POM.XMLAttribute(u'N', 1, 12, None)


attribVisible_url_1248271722030899344 = pycopia.XML.POM.XMLAttribute(u'visible_url', 1, 11, None)


attribFgcolor_2682975237200580100 = pycopia.XML.POM.XMLAttribute(u'fgcolor', 1, 11, None)


attribTag_4807433608964281 = pycopia.XML.POM.XMLAttribute(u'TAG', 1, 13, u'related:')


attribUrl_527219945134558641 = pycopia.XML.POM.XMLAttribute(u'url', 1, 11, None)


attribBgcolor_911213090796331684 = pycopia.XML.POM.XMLAttribute(u'bgcolor', 1, 11, None)


attribL_514968469437137296 = pycopia.XML.POM.XMLAttribute(u'L', 1, 13, u'1')


attribSe_2342063394331741609 = pycopia.XML.POM.XMLAttribute(u'SE', 1, 13, u'ISO-8859-1')


attribVer_564243035711265625 = pycopia.XML.POM.XMLAttribute(u'VER', 1, 11, None)


attribEn_3408712189162198416 = pycopia.XML.POM.XMLAttribute(u'EN', 1, 11, None)


attribEncoding_4404753610880238144 = pycopia.XML.POM.XMLAttribute(u'encoding', 1, 11, None)


attribN_3426581457697261824 = pycopia.XML.POM.XMLAttribute(u'N', 1, 11, None)


attribName_4287999358535244004 = pycopia.XML.POM.XMLAttribute(u'NAME', 1, 11, None)


attribTag_2177253955547847225 = pycopia.XML.POM.XMLAttribute(u'TAG', 1, 13, u'link:')


attribName_3839651748354608356 = pycopia.XML.POM.XMLAttribute(u'name', 1, 11, None)


attribQ_302809276911025921 = pycopia.XML.POM.XMLAttribute(u'q', 1, 11, None)


attribValue_94788037157002281 = pycopia.XML.POM.XMLAttribute(u'value', 1, 11, None)


attribV_431277155044170304 = pycopia.XML.POM.XMLAttribute(u'V', 1, 11, None)


attribMime_430583703186490441 = pycopia.XML.POM.XMLAttribute(u'MIME', 1, 13, u'text/html')


attribOriginal_value_2586052951233999844 = pycopia.XML.POM.XMLAttribute(u'original_value', 1, 11, None)


attribN1_209166773258746681 = pycopia.XML.POM.XMLAttribute(u'N1', 1, 12, None)


attribCtc_url_1628073390800683264 = pycopia.XML.POM.XMLAttribute(u'ctc_url', 1, 13, u'')


attribOdel_2778230957370838225 = pycopia.XML.POM.XMLAttribute(u'ODEL', 1, 11, None)


attribSz_1917534406987443556 = pycopia.XML.POM.XMLAttribute(u'SZ', 1, 11, None)


attribTag_25308272671347600 = pycopia.XML.POM.XMLAttribute(u'TAG', 1, 13, u'cache:')


attribEnc_1407847503510140004 = pycopia.XML.POM.XMLAttribute(u'ENC', 1, 13, u'')


attribSn_136224704229416100 = pycopia.XML.POM.XMLAttribute(u'SN', 1, 11, None)


attribFiltered_460884040604100 = pycopia.XML.POM.XMLAttribute(u'FILTERED', 1, 11, None)


attribValue_64774315446792169 = pycopia.XML.POM.XMLAttribute(u'VALUE', 1, 11, None)


attribCid_1664288556900978724 = pycopia.XML.POM.XMLAttribute(u'CID', 1, 13, u'')


attribRpos_212176399394949025 = pycopia.XML.POM.XMLAttribute(u'RPOS', 1, 11, None)


attribU_3329968306123005625 = pycopia.XML.POM.XMLAttribute(u'U', 1, 11, None)


attribType_1977399331530900489 = pycopia.XML.POM.XMLAttribute(u'type', 1, 11, None)




class Gsp(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'VER': attribVer_564243035711265625, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	KWATTRIBUTES = {
         'VER': attribVer_564243035711265625, 
         }
	_name = u'GSP'



_Root = Gsp



class Error(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'ERROR'


class Tm(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'TM'


class Q(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'Q'


class Cache(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'CACHE'


class Cache_url(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'CACHE_URL'


class Cache_redir_url(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'CACHE_REDIR_URL'


class Cache_last_modified(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'CACHE_LAST_MODIFIED'


class Cache_legend_found(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'CACHE_LEGEND_FOUND'


class Cache_legend_text(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'bgcolor': attribBgcolor_911213090796331684, 
         u'fgcolor': attribFgcolor_2682975237200580100, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	KWATTRIBUTES = {
         'bgcolor': attribBgcolor_911213090796331684, 
         'fgcolor': attribFgcolor_2682975237200580100, 
         }
	_name = u'CACHE_LEGEND_TEXT'


class Cache_legend_notfound(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'CACHE_LEGEND_NOTFOUND'


class Cache_content_type(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'CACHE_CONTENT_TYPE'


class Cache_language(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'CACHE_LANGUAGE'


class Cache_encoding(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'CACHE_ENCODING'


class Cache_html(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'CACHE_HTML'


class Blob(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'encoding': attribEncoding_4404753610880238144, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	KWATTRIBUTES = {
         'encoding': attribEncoding_4404753610880238144, 
         }
	_name = u'BLOB'


class Param(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'name': attribName_3839651748354608356, 
         u'value': attribValue_94788037157002281, 
         u'original_value': attribOriginal_value_2586052951233999844, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel(None)
	KWATTRIBUTES = {
         'name': attribName_3839651748354608356, 
         'value': attribValue_94788037157002281, 
         'original_value': attribOriginal_value_2586052951233999844, 
         }
	_name = u'PARAM'


class Cb(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'name': attribName_3839651748354608356, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	KWATTRIBUTES = {
         'name': attribName_3839651748354608356, 
         }
	_name = u'CB'


class Cs(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'name': attribName_3839651748354608356, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	KWATTRIBUTES = {
         'name': attribName_3839651748354608356, 
         }
	_name = u'CS'


class Ct(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'CT'


class Tt(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'TT'


class Gm(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'GM'


class Gl(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'GL'


class Gd(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'GD'


class Isurl(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel(None)
	_name = u'ISURL'


class Rpb(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel(None)
	_name = u'RPB'


class Bpb(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel(None)
	_name = u'BPB'


class Spelling(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'Spelling'


class Suggestion(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'q': attribQ_302809276911025921, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	KWATTRIBUTES = {
         'q': attribQ_302809276911025921, 
         }
	_name = u'Suggestion'


class Calc(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'CALC'


class Rhs(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'RHS'


class Lhs(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'LHS'


class Relatedsearches(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'RelatedSearches'


class Relatedsearch(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'RelatedSearch'


class Synonyms(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'Synonyms'


class Onesynonym(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'q': attribQ_302809276911025921, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	KWATTRIBUTES = {
         'q': attribQ_302809276911025921, 
         }
	_name = u'OneSynonym'


class News(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'NEWS'


class Source(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'SOURCE'


class Date(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'DATE'


class Maps(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'MAPS'


class Map(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'MAP'


class Dictionary(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'DICTIONARY'


class Word(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'WORD'


class Definitions(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'DEFINITIONS'


class Definition(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'MIME': attribMime_430583703186490441, 
         u'N': attribN_3426581457697261824, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	KWATTRIBUTES = {
         'MIME': attribMime_430583703186490441, 
         'N': attribN_3426581457697261824, 
         }
	_name = u'DEFINITION'


class Definition_term(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'DEFINITION_TERM'


class Definition_defn(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'DEFINITION_DEFN'


class Definition_language(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'DEFINITION_LANGUAGE'


class Definition_extension(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'MIME': attribMime_430583703186490441, 
         u'N': attribN_3426581457697261824, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	KWATTRIBUTES = {
         'MIME': attribMime_430583703186490441, 
         'N': attribN_3426581457697261824, 
         }
	_name = u'DEFINITION_EXTENSION'


class Definition_other_language(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'MIME': attribMime_430583703186490441, 
         u'N': attribN_3426581457697261824, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	KWATTRIBUTES = {
         'MIME': attribMime_430583703186490441, 
         'N': attribN_3426581457697261824, 
         }
	_name = u'DEFINITION_OTHER_LANGUAGE'


class Local_listings(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'LOCAL_LISTINGS'


class Local_listing(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'LOCAL_LISTING'


class Prose_results(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'PROSE_RESULTS'


class Prose_main(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'PROSE_MAIN'


class Prose_addl(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'PROSE_ADDL'


class Body_line(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'BODY_LINE'


class Block(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'BLOCK'


class N(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'N'


class Address(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'ADDRESS'


class Phone_number(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'PHONE_NUMBER'


class Distance_away(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'DISTANCE_AWAY'


class Image_thumbs(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'IMAGE_THUMBS'


class Image_thumb(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'IMAGE_THUMB'


class Image_source(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'IMAGE_SOURCE'


class Image_height(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'IMAGE_HEIGHT'


class Image_width(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'IMAGE_WIDTH'


class Froogle_listings(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'FROOGLE_LISTINGS'


class One_froogle(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'ONE_FROOGLE'


class Price(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'PRICE'


class Merchant(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'MERCHANT'


class Scholar_listings(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'SCHOLAR_LISTINGS'


class One_scholar(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'ONE_SCHOLAR'


class Scholar_author(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'SCHOLAR_AUTHOR'


class Scholar_citations(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'SCHOLAR_CITATIONS'


class Print_listings(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'PRINT_LISTINGS'


class One_print(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'ONE_PRINT'


class Print_author(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'PRINT_AUTHOR'


class Print_pages(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'PRINT_PAGES'


class Ads(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'ADS'


class Ad(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'url': attribUrl_527219945134558641, 
         u'ctc_url': attribCtc_url_1628073390800683264, 
         u'visible_url': attribVisible_url_1248271722030899344, 
         u'type': attribType_1977399331530900489, 
         u'n': attribN_1304866719271601641, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	KWATTRIBUTES = {
         'url': attribUrl_527219945134558641, 
         'ctc_url': attribCtc_url_1628073390800683264, 
         'visible_url': attribVisible_url_1248271722030899344, 
         'type': attribType_1977399331530900489, 
         'n': attribN_1304866719271601641, 
         }
	_name = u'AD'


class Line1(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'LINE1'


class Line2(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'LINE2'


class Line3(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'LINE3'


class Cpc(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'CPC'


class Wcpc(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'WCPC'


class Pcpm(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'PCPM'


class Regionname(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'REGIONNAME'


class Commercial(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'COMMERCIAL'


class Res(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'FILTERED': attribFiltered_460884040604100, 
         u'EN': attribEn_3408712189162198416, 
         u'SN': attribSn_136224704229416100, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	KWATTRIBUTES = {
         'FILTERED': attribFiltered_460884040604100, 
         'EN': attribEn_3408712189162198416, 
         'SN': attribSn_136224704229416100, 
         }
	_name = u'RES'


class M(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'M'


class Fi(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel(None)
	_name = u'FI'


class Xt(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel(None)
	_name = u'XT'


class Nb(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'NB'


class Pu(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'PU'


class Nu(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'NU'


class R(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'N1': attribN1_209166773258746681, 
         u'MIME': attribMime_430583703186490441, 
         u'L': attribL_514968469437137296, 
         u'N': attribN_4095895239692176041, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	KWATTRIBUTES = {
         'N1': attribN1_209166773258746681, 
         'MIME': attribMime_430583703186490441, 
         'L': attribL_514968469437137296, 
         'N': attribN_4095895239692176041, 
         }
	_name = u'R'


class U(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'U'


class Ue(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'UE'


class Ut(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'UT'


class Ute(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'UTE'


class Ud(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'UD'


class T(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'T'


class Rk(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'RK'


class Localinfo(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'LOCALINFO'


class Localquery(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'LOCALQUERY'


class Latlng_param(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'LATLNG_PARAM'


class Bn(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'BN'


class Ph(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'PH'


class Addr(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'ADDR'


class Citystate(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'CITYSTATE'


class Zip(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'ZIP'


class Latitude(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'LATITUDE'


class Longitude(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'LONGITUDE'


class Radius(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'RADIUS'


class Crawldate(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'CRAWLDATE'


class Xp(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'XP'


class Fs(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'NAME': attribName_4287999358535244004, 
         u'VALUE': attribValue_64774315446792169, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel(None)
	KWATTRIBUTES = {
         'NAME': attribName_4287999358535244004, 
         'VALUE': attribValue_64774315446792169, 
         }
	_name = u'FS'


class F(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'F'


class S(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'S'


class Lang(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'LANG'


class Has(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'HAS'


class Debug(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'DEBUG'


class Ind_debug(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'IND_DEBUG'


class Doc_debug(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'DOC_DEBUG'


class Di(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'DI'


class Cat(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'SE': attribSe_2342063394331741609, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	KWATTRIBUTES = {
         'SE': attribSe_2342063394331741609, 
         }
	_name = u'CAT'


class Gn(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'GN'


class Fvn(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'FVN'


class Dt(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'DT'


class Ds(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'DS'


class L(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'TAG': attribTag_2177253955547847225, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel(None)
	KWATTRIBUTES = {
         'TAG': attribTag_2177253955547847225, 
         }
	_name = u'L'


class C(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'SZ': attribSz_1917534406987443556, 
         u'TAG': attribTag_25308272671347600, 
         u'ENC': attribEnc_1407847503510140004, 
         u'CID': attribCid_1664288556900978724, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel(None)
	KWATTRIBUTES = {
         'SZ': attribSz_1917534406987443556, 
         'TAG': attribTag_25308272671347600, 
         'ENC': attribEnc_1407847503510140004, 
         'CID': attribCid_1664288556900978724, 
         }
	_name = u'C'


class Rt(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'TAG': attribTag_4807433608964281, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel(None)
	KWATTRIBUTES = {
         'TAG': attribTag_4807433608964281, 
         }
	_name = u'RT'


class Pers_cats(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'PERS_CATS'


class Hn(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'U': attribU_3329968306123005625, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	KWATTRIBUTES = {
         'U': attribU_3329968306123005625, 
         }
	_name = u'HN'


class Mt(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'V': attribV_431277155044170304, 
         u'N': attribN_3426581457697261824, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel(None)
	KWATTRIBUTES = {
         'V': attribV_431277155044170304, 
         'N': attribN_3426581457697261824, 
         }
	_name = u'MT'


class Revs(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'RPOS': attribRpos_212176399394949025, 
         u'ODEL': attribOdel_2778230957370838225, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	KWATTRIBUTES = {
         'RPOS': attribRpos_212176399394949025, 
         'ODEL': attribOdel_2778230957370838225, 
         }
	_name = u'REVS'


class Fq(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'FQ'


class Rev(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'N': attribN_4095895239692176041, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	KWATTRIBUTES = {
         'N': attribN_4095895239692176041, 
         }
	_name = u'REV'


class Car(pycopia.XML.POM.ElementNode):
	CONTENTMODEL = pycopia.XML.POM.ContentModel((True,))
	_name = u'CAR'


class Md(pycopia.XML.POM.ElementNode):
	ATTRIBUTES = {
         u'V': attribV_431277155044170304, 
         u'N': attribN_3426581457697261824, 
         }
	CONTENTMODEL = pycopia.XML.POM.ContentModel(None)
	KWATTRIBUTES = {
         'V': attribV_431277155044170304, 
         'N': attribN_3426581457697261824, 
         }
	_name = u'MD'


GENERAL_ENTITIES = {}

# Cache for dynamic classes for this dtd.


_CLASSCACHE = {}

