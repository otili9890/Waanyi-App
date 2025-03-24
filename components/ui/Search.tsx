import React, { useState } from "react";
import { StyleSheet, Text, View, FlatList, Button } from "react-native";
import { ListItem, Overlay, SearchBar } from "react-native-elements";
import ItemOverlay from '@/components/ui/ItemOverlay';
import filter from "lodash.filter";

const DATA = require("../../assets/data/waanyi.json");

export default function Search () {
  const [searchQuery, setSearchQuery] = useState("");
  const [data, setData] = useState(DATA);
  const [fullData, setFullData] = useState(DATA);
  const [item, setItem] = useState("");
  const [visible, setVisible] = useState(false);

  const toggleOverlay = () => {
    setVisible(!visible);
  };

  const searchFunction = (query: string) => {
    setSearchQuery(query);
    const formattedQuery = query.toLowerCase();
    const filteredData = filter(fullData, (item: any) => {
      return contains(item, formattedQuery);
    })
    setData(filteredData)
  };

  // Formats the English Gloss is its an array
  const processList = (obj: any) =>{
    if (obj instanceof Array && obj.length > 0) {
      let list = '';
      obj.forEach((e, idx) => {
        list += e;
        if (idx < obj.length - 1) {
          list += ', ';
        }
      });
      list += '.';
      return list;
    } else {
      return obj;
    }
  }

  // Check if the id or English_Gloss contains the query
  const contains = ({id, English_Gloss}: any, query: string) => {
    if (id.toLowerCase().includes(query) || English_Gloss.includes(query)) {
      return true;
    }
    // If English_Gloss is an array checks through array
    if (English_Gloss instanceof Array && English_Gloss.length > 0) {
      if (id.toLowerCase().includes(query) || English_Gloss.some((e) => e.toLowerCase().includes(query))) {
        return true;
      }
    }  
    return false;
  }

  type ItemProps = {
    id: string;
    item: any;
    onPress: () => void;
  };

  // Item which is rendered throughout the FlatList
  const Item = ({ id, item, onPress }: ItemProps) => {
    return (
      <ListItem key={id} onPress={onPress} style={styles.item}>
        <Text>{id}</Text>
        <Text>{processList(item.English_Gloss)}</Text>
      </ListItem>
    );
  };
  
  const renderItem = ({ item }: any) => <Item id={item.id} item={item} onPress={function() { setItem(item); setVisible(true)}} />;

  return (
    <View style={styles.container}>
      <Overlay isVisible={visible} onBackdropPress={toggleOverlay} style={styles.overlay}>
        <Text>{item.id}</Text>
        <Text>Part of speech: {item.Part_of_Speech}</Text>
        <Text>English_Gloss: {item.English_Gloss}</Text>
        <Text>Definition: {item.Definition}</Text>
        <Button onPress={toggleOverlay} title="Exit" />
      </Overlay>
      <SearchBar
        style={styles.search}
        placeholder="Search Here..."
        lightTheme
        clearButtonMode="always"
        round
        value={searchQuery}
        onChangeText={(text) => searchFunction(text)}
        autoCorrect={false}
      />
      <FlatList
        data={data}
        renderItem={renderItem}
        ListFooterComponent={() => <Text>Footer</Text>}
        keyExtractor={(item) => item.id}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: "red",
    marginTop: 30,
    padding: 2,
  },
  item: {
    color: "white",
    marginVertical: 8,
    marginHorizontal: 16,
  },
  search: {
    backgroundColor: "none",
  },
  overlay: {
    backgroundColor: "purple",
    width: "90%",
    height: "90%",
    padding: 10
  }
});
