import math

class QuadTreeNode:
    def __init__(self, boundary):
        self.boundary = boundary
        self.points = []
        self.children = [None, None, None, None]  # NW, NE, SW, SE

class QuadTree:
    def __init__(self, boundary):
        self.root = QuadTreeNode(boundary)

    def insert(self, point):
        self._insert_recursive(self.root, point)

    def _insert_recursive(self, node, point):
        if not node.boundary.contains_point(point):
            return False

        if len(node.points) < 4 and not any(node.children):
            node.points.append(point)
            return True

        if not any(node.children):
            self._subdivide(node)

        for i, child in enumerate(node.children):
            if self._insert_recursive(child, point):
                return True

    def _subdivide(self, node):
        x, y, w, h = node.boundary.x, node.boundary.y, node.boundary.w / 2, node.boundary.h / 2
        node.children[0] = QuadTreeNode(Boundary(x, y, w, h))
        node.children[1] = QuadTreeNode(Boundary(x + w, y, w, h))
        node.children[2] = QuadTreeNode(Boundary(x, y + h, w, h))
        node.children[3] = QuadTreeNode(Boundary(x + w, y + h, w, h))

        for point in node.points:
            for child in node.children:
                self._insert_recursive(child, point)
        node.points = []

    def query(self, boundary):
        return self._query_recursive(self.root, boundary)

    def _query_recursive(self, node, boundary):
        result = []
        if not node.boundary.intersects_boundary(boundary):
            return result

        for point in node.points:
            if boundary.contains_point(point):
                result.append(point)

        if any(node.children):
            for child in node.children:
                result.extend(self._query_recursive(child, boundary))

        return result

    def remove_point(self, point, node=None):
        if node is None:
            node = self.root

        if point in node.points:
            node.points.remove(point)

        for child in node.children:
            if child and child.boundary.contains_point(point):
                self.remove_point(point, child)

    def _remove_point_recursive(self, node, point):
        if point in node.points:
            node.points.remove(point)
            return True

        for child in node.children:
            if self._remove_point_recursive(child, point):
                return True

        return False

class Boundary:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains_point(self, point):
        return (self.x <= point[0] < self.x + self.w) and (self.y <= point[1] < self.y + self.h)

    def intersects_boundary(self, other_boundary):
        return not (self.x + self.w <= other_boundary.x or
                    other_boundary.x + other_boundary.w <= self.x or
                    self.y + self.h <= other_boundary.y or
                    other_boundary.y + other_boundary.h <= self.y)

# 재료 좌표
coords = {
    "통통 연꽃": [(66,155),(37,176),(72,206),(237,555),(230,563),(180,569),(494,523),(494,528),(494,527),(493,527),(680,360),(680,359),(813,476),(799,447),(827,404),(832,392),(600,574),(597,573),(731,789),(732,789),(727,799),(726,799),(697,794),(685,783),(684,785),(684,781),(689,779),(693,775),(694,776),(695,775),(718,769),(715,776),(716,777),(179,975),(260,1031),(262,1031),(235,1190),(235,1181),(308,1072),(307,1078),(383,931),(377,933),(378,933),(409,1119),(414,1116),(415,1115),(944,1182),(946,1183),(959,1165),(958,1164),(1039,1135),(1034,1122),(1034,1121)],
    "세실리아꽃": [(292,1224),(290,1229),(290,1231),(267,1239),(266,1240),(266,1241),(234,1258),(234,1261),(232,1259),(231,1260),(220,1273),(221,1272),(223,1273),(223,1276),(217,1288),(218,1289),(221,1289),(250,1260),(252,1260),(250,1258),(279,1260),(275,1277),(275,1275),(276,1276),(277,1276),(294,1273),(297,1274),(309,1264),(310,1263),(327,1278),(328,1279),(330,1290),(327,1338),(332,1341),(329,1343),(328,1343),(325,1342)],
    "민들레 씨앗": [(390,452),(387,453),(630,508),(607,472),(552,469),(627,639),(769,560),(770,560),(628,814),(505,956),(504,957),(534,1278),(528,1279),(528,1276),(317,1182),(317,1185),(318,1185),(285,1011),(287,1011),(292,1003),(227,900),(118,955),(0,1264),(776,1112),(761,1007),(761,1003),(964,1245),(854,1255),(852,1256),(910,1461),(905,1455),(475,806),(468,805),(467,810),(447,825),(444,828),(440,824),(435,825),(392,821),(363,781),(835,316),(836,311),(828,317),(799,339),(807,281),(798,292),(776,298),(785,273),(789,271),(786,265)],
    "바람버섯": [(751,539),(754,543),(767,516),(769,516),(769,474),(777,466),(769,472),(626,760),(616,756),(621,756),(638,759),(662,756),(658,754),(646,790),(641,803),(637,802),(624,803),(624,805),(617,811),(607,810),(606,809),(604,804),(605,799),(459,702),(461,704),(463,704),(465,702),(464,701),(464,700),(450,731),(454,747),(454,749),(456,749),(453,747),(473,761),(471,764),(470,764),(464,772),(464,773),(469,783),(465,784),(462,783),(415,800),(414,803),(406,800),(402,798),(395,798),(381,760),(378,738),(400,735),(408,736)],
    "등불꽃": [(80,164),(47,206),(192,504),(194,504),(194,503),(399,429),(401,430),(403,428),(402,428),(393,388),(390,388),(391,387),(312,453),(488,568),(486,568),(487,570),(526,536),(528,536),(523,522),(462,524),(461,524),(468,534),(469,533),(460,499),(459,498),(530,336),(531,337),(532,333),(662,315),(661,312),(665,313),(666,311),(269,1159),(269,1160),(301,1176),(301,1177),(302,1178),(426,1250),(424,1248),(424,1253),(423,1252),(422,1252),(583,1158),(577,1164),(582,1167),(574,1178),(566,1174),(568,1185),(790,971),(791,971),(759,999),(761,982),(749,974),(740,949),(723,941),(715,930),(714,949),(411,939),(410,941),(411,942),(395,941),(396,940),(366,937),(365,937),(364,937),(370,907),(369,909),(367,904),(367,903),(364,907),(360,895),(357,895),(346,898),(345,900)],
    "낙락베리": [(181,1026),(127,994),(174,947),(223,913),(201,887),(116,878),(117,927),(18,989),(0,1082),(75,1052),(79,1116),(135,1092),(174,1062),(181,1107),(183,1134),(30,1215),(24,1274),(25,1300),(78,1351)],
    "풍차 국화": [(228,1026),(227,1026),(630,983),(628,979),(619,990),(619,989),(611,986),(610,986),(597,1037),(626,1047),(628,1048),(630,1047),(648,1091),(647,1092),(711,1105),(713,1103),(713,1105),(664,1009),(661,1007),(660,1007),(661,1002),(679,584),(680,578),(681,578),(679,576),(665,568),(664,568),(660,589),(663,589),(664,590),(102,250),(105,249),(106,248),(106,244),(84,184),(80,184),(81,183),(79,182),(53,126),(51,127),(50,124),(49,125),(27,138),(24,139),(25,136),(253,32),(254,32),(254,31),(218,71),(217,70),(218,69),(263,80),(266,80),(295,74),(296,73),(294,72),(289,61),(263,184),(261,184),(263,188),(269,261),(266,262),(264,260),(265,259)],
    "고리고리 열매": [(479,502),(494,495),(495,496),(532,476),(540,474),(546,463),(544,457),(545,458),(551,452),(560,437),(563,430),(565,430),(573,447),(574,455),(573,455),(558,470),(558,471),(560,473),(562,474),(572,456),(573,457),(585,438),(596,461),(575,474),(567,487),(558,520),(624,403),(623,401),(627,386),(627,378),(618,372),(617,371),(616,370)],
}

from PIL import Image

im = Image.open('images/map.png')
width, height = im.size
selected_collection = None

# 쿼드트리 초기화
quadtree = QuadTree(Boundary(0, 0, width, height))

def change_find_collection(collection):
    global selected_collection
    selected_collection = collection
    
    global quadtree
    quadtree = QuadTree(Boundary(0, 0, width, height))
        
    if selected_collection != None:
        for collection_coord in coords[selected_collection]:
            quadtree.insert(collection_coord)
        
def get_selected_collection():
    return selected_collection

# 가장 가까운 재료를 찾는 함수
def find_closest_collection(my_position):
    search_boundary = Boundary(my_position[0] - 2000, my_position[1] - 2000, 4000, 4000)
    nearby_collections = quadtree.query(search_boundary)
    min_distance = float('inf')
    distance = -1
    closest_collection = None

    for _, collection in enumerate(nearby_collections):
        distance = math.sqrt((collection[0] - my_position[0]) ** 2 + (collection[1] - my_position[1]) ** 2)
        if distance < min_distance:
            min_distance = distance
            closest_collection = collection

    # 내 위치와 가장 가까운 재료가 동일한 경우
    if closest_collection is not None and \
       closest_collection[0] - 1 <= my_position[0] <= closest_collection[0] + 1 and \
       closest_collection[1] - 1 <= my_position[1] <= closest_collection[1] + 1:
        print("Collected")
        # 재료 배열에서 해당 재료 좌표 삭제
        quadtree.remove_point(closest_collection)
        # 전역 변수 coords에서도 해당 좌표를 삭제
        coords[get_selected_collection()].remove(closest_collection)
        
    return (closest_collection, min_distance)



if __name__ == "__main__":
    # 내 위치 (외부에서 전달)
    my_position = (510,774)
    
    change_find_collection("풍차 국화")

    # 가장 가까운 재료의 위치 찾기
    closest_treasure = find_closest_collection(my_position)
    print("가장 가까운 재료의 위치:", closest_treasure)
